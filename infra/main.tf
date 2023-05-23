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

resource "aws_s3_bucket" "COBI_athena_results_2023" {
  bucket = "COBI-athena-results-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_model_2023" {
  bucket = "COBI-model-2023"
  acl    = "private"
}

resource "aws_lambda_function" "copernicus_extract" {
  filename = copernicus_extract.zip
  function_name = "copernicus_extract"
  role = aws_iam_role.lambda_exec.arn
  handler = "copernicus_extract.lambda_handler"
  runtime = "python3.8"
}
