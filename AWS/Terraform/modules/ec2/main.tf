locals {
  command = <<EOF
    VolID=$(aws ec2 describe-volumes --region $REGION --filters Name=attachment.instance-id,Values=$EC2ID | jq -r '.Volumes[0].Attachments[0].VolumeId')
    #echo "VolID: $VolID"
    VolSize=$(aws ec2 describe-volumes --region $REGION --volume-id $VolID | jq '.Volumes[0].Size')
    #echo "VolSize: $VolSize + 1 -> $((VolSize+1))"
    aws ec2 modify-volume --region $REGION --volume-id $VolID --size $((VolSize+1))
    EOF
}

resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  })

  tags = {
      tag-key = "${var.namespace}-EC2-Role"
  }
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = "${aws_iam_role.ec2_role.name}"
}

resource "aws_iam_role_policy" "EBSVolumeAccess" {
  name = "EBSVolumeAccess"
  role = "${aws_iam_role.ec2_role.id}"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:ModifyVolume"
            ],
            "Resource": "*",
            "Condition": {
                "ArnEquals": {
                    "ec2:SourceInstanceARN": "arn:aws:ec2:*:*:instance/${aws_instance.ec2_bastion.id}"
                }
            }
        }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "AmazonS3ReadOnlyAccess" {
  role       = "${aws_iam_role.ec2_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_instance" "ec2_bastion" {
  ami                         = var.ami_id
  associate_public_ip_address = true
  instance_type               = "t2.micro"
  key_name                    = var.key_name
  subnet_id                   = var.vpc1.public_subnets[0]
  vpc_security_group_ids      = [var.vpc1_sg_public_id]
  iam_instance_profile        = "${aws_iam_instance_profile.ec2_profile.name}"
  user_data                   = "${file("${path.module}/../scripts/bastion.sh")}"
  connection {
    type = "ssh"
    user = "ec2-user"
    host = self.public_ip
    timeout = "1m"
    private_key = "${file("${path.module}/../../${var.namespace}-key.pem")}"
  }
  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    environment = {
      REGION = "${var.region}"
      EC2ID = "${self.id}"
    }
    command = local.command
  }
  provisioner "remote-exec" {
    inline = [
      "sudo growpart /dev/xvda 1",
      "sudo xfs_growfs -d /"
    ]
  }
  tags = {
    "Name"        = "${var.namespace}-EC2-BASTION"
    "owner"       = "${var.owner}"
    "project"     = "${var.project}"
    "environment" = "${var.environment}"
  }
  volume_tags = {
    "Name"        = "${var.namespace}-VOL-BASTION"
    "owner"       = "${var.owner}"
    "project"     = "${var.project}"
    "environment" = "${var.environment}"
  }
}

resource "aws_instance" "ec2_host1" {
  ami                         = var.ami_id
  instance_type               = "t2.micro"
  key_name                    = var.key_name
  subnet_id                   = var.vpc2.private_subnets[0]
  vpc_security_group_ids      = [var.vpc2_sg_private_id]
  iam_instance_profile        = "${aws_iam_instance_profile.ec2_profile.name}"
  user_data                   = "${file("${path.module}/../scripts/nginx.sh")}"
  tags = {
    "Name"        = "${var.namespace}-EC2-HOST1"
    "owner"       = "${var.owner}"
    "project"     = "${var.project}"
    "environment" = "${var.environment}"
  }
  volume_tags = {
    "Name"        = "${var.namespace}-VOL-HOST1"
    "owner"       = "${var.owner}"
    "project"     = "${var.project}"
    "environment" = "${var.environment}"
  }
}

resource "aws_instance" "ec2_host2" {
  ami                         = var.ami_id
  instance_type               = "t2.micro"
  key_name                    = var.key_name
  subnet_id                   = var.vpc2.private_subnets[1]
  vpc_security_group_ids      = [var.vpc2_sg_private_id]
  iam_instance_profile        = "${aws_iam_instance_profile.ec2_profile.name}"
  user_data                   = "${file("${path.module}/../scripts/nginx.sh")}"
  tags = {
    "Name"        = "${var.namespace}-EC2-HOST2"
    "owner"       = "${var.owner}"
    "project"     = "${var.project}"
    "environment" = "${var.environment}"
  }
  volume_tags = {
    "Name"        = "${var.namespace}-VOL-HOST2"
    "owner"       = "${var.owner}"
    "project"     = "${var.project}"
    "environment" = "${var.environment}"
  }
}