import boto3

ec2_resource = boto3.resource('ec2')
for instance in ec2_resource.instances.all():
    for volume in instance.volumes.all():
        instance_tags = [tag for tag in instance.tags]
        instance_tags_keys = [tag['Key'] for tag in instance.tags]
        volume_tags = [tag for tag in volume.tags]
        volume_tags_keys = [tag['Key'] for tag in volume.tags]
        if instance_tags_keys not in volume_tags_keys:
            volume.create_tags(DryRun = False, Tags = instance_tags)