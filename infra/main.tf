provider "aws" {
  region  = "us-east-2"
}

module "buckets" {
  source = "./buckets"
}

