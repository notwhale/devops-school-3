resource "aws_iam_group" "workgroup" {
  name = "WorkGroup"
}

resource "aws_iam_policy" "deny_without_tags" {
  name        = "DenyWithoutTags"
  description = "Deny create EC2 and EBS without tags"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowDescribeAll",
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowRunInstances",
            "Effect": "Allow",
            "Action": "ec2:RunInstances",
            "Resource": [
                "arn:aws:ec2:*::image/*",
                "arn:aws:ec2:*::snapshot/*",
                "arn:aws:ec2:*:*:subnet/*",
                "arn:aws:ec2:*:*:network-interface/*",
                "arn:aws:ec2:*:*:security-group/*",
                "arn:aws:ec2:*:*:key-pair/*"
            ]
        },
        {
            "Sid": "DenyWithoutTags",
            "Effect": "Deny",
            "Action": [
                "ec2:CreateVolume",
                "ec2:RunInstances"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:volume/*",
                "arn:aws:ec2:*:*:instance/*"
            ],
            "Condition": {
                "ForAllValues:StringNotLike": {
                    "aws:TagKeys": [
                        "owner",
                        "project",
                        "environment"
                    ]
                }
            }
        },
        {
            "Sid": "AllowRunInstancesCreateVolume",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateVolume",
                "ec2:RunInstances"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:volume/*",
                "arn:aws:ec2:*:*:instance/*"
            ]
        },
        {
            "Sid": "AllowCreateTagsOnRunInstance",
            "Effect": "Allow",
            "Action": "ec2:CreateTags",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "ec2:CreateAction": "RunInstances"
                }
            }
        }
    ]
  })
}

resource "aws_iam_policy_attachment" "workgroup_attachment" {
  name       = "WorkGroupAttachment"
  groups     = [aws_iam_group.workgroup.name]
  policy_arn = aws_iam_policy.deny_without_tags.arn
}

resource "aws_iam_role" "ec2_role" {
  name = "EC2Role"

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
      tag-key = "${var.namespace}-EC2Role"
  }
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2Profile"
  role = "${aws_iam_role.ec2_role.name}"
}

resource "aws_iam_role_policy" "ebs_volume_access" {
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
                    "ec2:SourceInstanceARN": "arn:aws:ec2:*:*:instance/${var.bastion_id}"
                }
            }
        }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "amazon_s3_read_only_access" {
  role       = "${aws_iam_role.ec2_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}