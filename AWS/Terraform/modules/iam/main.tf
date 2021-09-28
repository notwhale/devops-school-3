resource "aws_iam_group" "Work" {
  name = "Work"
}

resource "aws_iam_policy_attachment" "group_attachment" {
  name       = "group_attachment"
  groups     = [aws_iam_group.Work.name]
  policy_arn = aws_iam_policy.DenyWithoutTags.arn
}

resource "aws_iam_policy" "DenyWithoutTags" {
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