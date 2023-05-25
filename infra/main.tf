provider "aws" {
  region  = "us-east-2"
}

resource "aws_s3_bucket" "COBI_landing_zone_2023" {
  bucket = "cobi-landing-zone-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_input_data_2023" {
  bucket = "cobi-input-data-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_clean_data_2023" {
  bucket = "cobi-clean-data-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_athena_results_2023" {
  bucket = "cobi-athena-results-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_model_2023" {
  bucket = "cobi-model-2023"
  acl    = "private"
}

resource "aws_s3_bucket" "COBI_lambda_layers_2023" {
  bucket = "cobi-lambda-layers-2023"
  acl    = "private"
}

# upload Copernicus variable dictionary to S3
resource "aws_s3_bucket_object" "copernicus_var_dict" {
  bucket = aws_s3_bucket.COBI_landing_zone_2023.id
  key    = "copernicus_var_dict.csv" #path to the csv file
  source = "./input_data/copernicus_var_dict.csv" #path to the csv file
}

# upload Lambda layers to S3
resource "aws_s3_bucket_object" "layer_requests" {
  bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
  key    = "layer_requests.zip" #path to the zip file
  source = "./lambda_layers/layer_requests.zip" #path to the zip file
}

resource "aws_s3_bucket_object" "layer_xarray" {
  bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
  key    = "layer_xarray.zip" #path to the zip file
  source = "./lambda_layers/layer_xarray.zip" #path to the zip file
}

resource "aws_s3_bucket_object" "layer_motu" {
  bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
  key    = "layer_motu.zip" #path to the zip file
  source = "./lambda_layers/layer_motu.zip" #path to the zip file
}
###

# create Lambda layers
resource "aws_lambda_layer_version" "layer_requests" {
  layer_name = "layer_requests"
  s3_bucket  = "cobi-lambda-layers-2023"
  s3_key     = "layer_requests.zip"
  compatible_runtimes = ["python3.8"]
  description = "Python layer for x86_64 architecture and Python 3.8"

}

resource "aws_lambda_layer_version" "layer_xarray" {
  layer_name = "layer_xarray"
  s3_bucket  = "cobi-lambda-layers-2023"
  s3_key     = "layer_xarray.zip"
  compatible_runtimes = ["python3.8"]
  description = "Python layer for x86_64 architecture and Python 3.8" 

}
  
resource "aws_lambda_layer_version" "layer_motu" {
  layer_name = "layer_motu"
  s3_bucket  = "cobi-lambda-layers-2023"
  s3_key     = "layer_motu.zip"
  compatible_runtimes = ["python3.8"]
  description = "Python layer for x86_64 architecture and Python 3.8"

}
###




# resource "aws_lambda_function" "copernicus_extract" {
#   filename = copernicus_extract.zip
#   function_name = "copernicus_extract"
#   role = aws_iam_role.lambda_exec.arn
#   handler = "copernicus_extract.lambda_handler"
#   runtime = "python3.8"
# }
