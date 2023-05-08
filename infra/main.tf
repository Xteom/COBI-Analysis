provider "aws" {
  region  = "us-east-2"
}

module "buckets" {
  source = "./buckets"
}

resource "aws_s3_bucket" "COBI_landing_zone_2023" {
  bucket = "COBI-landing-zone-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_clean_data_2023" {
  bucket = "COBI-clean-data-2023"
  acl    = "private"
}

