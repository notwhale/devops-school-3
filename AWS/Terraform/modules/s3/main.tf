resource "aws_s3_bucket" "s3bucket" {
  acl    = "private"

  tags = {
    Name = "${var.namespace}-s3bucket"
  }

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    noncurrent_version_transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 90
    }

    noncurrent_version_expiration {
      days = 90
    }
  }
}