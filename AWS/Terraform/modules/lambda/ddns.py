import boto3
import sys
import time

ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')
r53_client = boto3.client('route53')

domain = "tf.internal."
ttl = 300

def lambda_handler(event, context):
    asg_name = event['detail']['autoscalinggroupname']
    record_set_name = asg_name + "." + domain
    event_region = event['region']
    for subnet in ec2_client.describe_subnets(subnetids=[event['detail']['details']['subnet id']])['subnets']:
        event_vpc_id = subnet['vpcid']
    print(f"{event['detail']['description']} in autoscaling group {asg_name} under vpc id {event_vpc_id}")
    # if hosted zone exists in route53 obtain its id.
    hosted_zone_id = get_hosted_zone_id(domain, event_vpc_id)
    if hosted_zone_id:
        print(f"hostedzone {domain} under vpc id {event_vpc_id} in region {event_region} exists in with id {hosted_zone_id}")
    # else hosted zone doesn't exist in route53 create it and obtain its id.
    else:
        print(f"hosted zone {domain} doesn't exists under vpc id {event_vpc_id} in region {event_region}. going to create it")
        hosted_zone_id = create_hosted_zone(domain, event_region, event_vpc_id)
        if hosted_zone_id:
            print(f"hostedzone {domain} under vpc id {event_vpc_id} in region {event_region} was created successfully with id {hosted_zone_id}")
        else:
            print(f"hostedzone {domain} under vpc id {event_vpc_id} in region {event_region} was already created by other instance of the lambda function - aborting")
            sys.exit()
    # obtain private ips of all active instances in the auto scaling group which triggered this event.
    servers = get_asg_private_ips(asg_name)
    # if there are private ips it means the autoscaling group exists and contains at least one active instances. create/update record set in route53 hosted zone.
    if servers:
        update_hosted_zone_records(hosted_zone_id, record_set_name, ttl, servers)
        print(f"record set {record_set_name} was created/updated successfully with the following a records {servers}")
    # if there are no private ips it means the autoscaling group was deleted or doesn't contain any active instances. remove record set from hosted zone in route53.
    else:
        print(f"auto scaling group {asg_name} does not exist or empty - going to remove relevent a records")
        delete_hosted_zone_records(hosted_zone_id, record_set_name)


def get_hosted_zone_id(domain, event_vpc_id):
    for hosted_zone in r53_client.list_hosted_zones()['HostedZones']:
        if hosted_zone['Name'] == domain and hosted_zone['Config']['PrivateZone'] == True:
            for vpc in r53_client.get_hosted_zone(Id = hosted_zone['Id'])['VPCs']:
                if vpc['VPCId'] == event_vpc_id:
                    return hosted_zone['Id']
    else:
        return False


def create_hosted_zone(domain, event_region, event_vpc_id):
    try:
        response = r53_client.create_hosted_zone(
            Name = domain,
            VPC = {
                'VPCRegion': str(event_region),
                'VPCId': event_vpc_id
            },
            CallerReference = str(time.time()),
            HostedZoneConfig = {
                'Comment': f"Created by Radware lambda fucntion for VPC {event_vpc_id} in region {event_region}",
                'PrivateZone': True
            }
        )
        return response['HostedZone']['Id']
    except:
        return False


def get_asg_private_ips(asg_name):
    for asg in asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])['AutoScalingGroups']:
        instance_ids = []
        for instance in asg['Instances']:
            if instance['LifecycleState'] == 'InService':
                instance_ids.append(instance['InstanceId'])
        if instance_ids:
            servers = []
            for reservation in ec2_client.describe_instances(InstanceIds = instance_ids)['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        servers.append({'Value': instance['PrivateIpAddress']})
            return servers


def update_hosted_zone_records(hosted_zone_id, record_set_name, ttl, servers):
    r53_client.change_resource_record_sets(
    HostedZoneId = hosted_zone_id,
    ChangeBatch = {
        'Changes': [
            {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': record_set_name,
                'Type': 'A',
                'TTL': ttl,
                'ResourceRecords': sorted(servers)[:28]
            }
        }]
    })
    return


def delete_hosted_zone_records(hosted_zone_id, record_set_name):
    for record_set in r53_client.list_resource_record_sets(HostedZoneId = hosted_zone_id)['ResourceRecordSets']:
        if record_set['Name'] == record_set_name:
            try:
                r53_client.change_resource_record_sets(
                HostedZoneId = hosted_zone_id,
                ChangeBatch = {
                    'Changes': [
                        {
                        'Action': 'DELETE',
                        'ResourceRecordSet': record_set
                    }]
                })
                print(f"Record set {record_set_name} removed successfully")
            except:
                print(f"Record set {record_set_name} was already removed by other instance of the lambda function")
            break
    else:
        print(f"Record set {record_set_name} was already removed by other instance of the lambda function")
