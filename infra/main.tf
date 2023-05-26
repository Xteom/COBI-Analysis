provider "aws" {
  region  = "us-east-2"
}

# S3 Buckets
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
###

# upload Copernicus historical data to S3
resource "aws_s3_object" "BioGeoChemicalOptics" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "BioGeoChemicalOptics.csv" #path to the csv file
  source = "./historical_copernicus/BioGeoChemicalOptics.csv" #path to the csv file
}

resource "aws_s3_object" "Plankton" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "Plankton.csv" #path to the csv file
  source = "./historical_copernicus/Plankton.csv" #path to the csv file
}

resource "aws_s3_object" "Reflectance" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "Reflectance.csv" #path to the csv file
  source = "./historical_copernicus/Reflectance.csv" #path to the csv file
}

resource "aws_s3_object" "SeaSurfaceTemperature" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "SeaSurfaceTemperature.csv" #path to the csv file
  source = "./historical_copernicus/SeaSurfaceTemperature.csv" #path to the csv file
}

resource "aws_s3_object" "TotalSurfaceaAnd15mCurrent" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "TotalSurfaceaAnd15mCurrent.csv" #path to the csv file
  source = "./historical_copernicus/TotalSurfaceaAnd15mCurrent.csv" #path to the csv file
}

resource "aws_s3_object" "Transparence" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "Transparence.csv" #path to the csv file
  source = "./historical_copernicus/Transparence.csv" #path to the csv file
}

resource "aws_s3_object" "WaveHeight" {
  bucket = aws_s3_bucket.COBI_clean_data_2023.id
  key    = "WaveHeight.csv" #path to the csv file
  source = "./historical_copernicus/WaveHeight.csv" #path to the csv file
}
###

# upload Copernicus variable dictionary to S3
resource "aws_s3_object" "copernicus_var_dict" {
  bucket = aws_s3_bucket.COBI_input_data_2023.id
  key    = "copernicus_var_dict.csv" #path to the csv file
  source = "./input_data/copernicus_var_dict.csv" #path to the csv file
}
###

# # Create ECR repositories
# this code was supposed to create ECR repositories for the Lambda functions and the upload the images to them
# still figuring out how to do it, so for now I'm just uploading the images manually
# resource "aws_ecr_repository" "copernicus_extract_lambda" {
#   name = "copernicus_extract_lambda"
# }

# resource "aws_ecr_repository" "copernicus_transform_lambda" {
#   name = "copernicus_transform_lambda"
# }
# ###

# # upload Lambda code to ECR
# resource "null_resource" "execute_script"{
#   provisioner "local-exec" {
#     command = <<EOF
#       current_dir=$(pwd)
#       cd ./lambdas/lambda_images/copernicus_extract_lambda && upload_ecr.sh
#       cd ../copernicus_transform_lambda && upload_ecr.sh && upload_ecr.sh
#       cd $current_dir
#     EOF
#   }
# }
# ###

# upload Lambda layers to S3
resource "aws_s3_object" "layer_requests" {
  bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
  key    = "layer_requests.zip" #path to the zip file
  source = "./lambdas/lambda_layers/layer_requests.zip" #path to the zip file
}

# resource "aws_s3_object" "layer_xarray" {
#   bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
#   key    = "layer_xarray.zip" #path to the zip file
#   source = "./lambda_layers/layer_xarray.zip" #path to the zip file
# }

# resource "aws_s3_object" "layer_motu" {
#   bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
#   key    = "layer_motu.zip" #path to the zip file
#   source = "./lambda_layers/layer_motu.zip" #path to the zip file
# }

# resource "aws_s3_object" "layer_numpy" {
#   bucket = aws_s3_bucket.COBI_lambda_layers_2023.id
#   key    = "layer_numpy.zip" #path to the zip file
#   source = "./lambda_layers/layer_numpy/python.zip" #path to the zip file
# }

###

# create Lambda layers
resource "aws_lambda_layer_version" "layer_requests" {
  layer_name = "layer_requests"
  s3_bucket  = "cobi-lambda-layers-2023"
  s3_key     = "layer_requests.zip"
  compatible_runtimes = ["python3.8"]
  description = "Python layer for x86_64 architecture and Python 3.8"

}

# resource "aws_lambda_layer_version" "layer_xarray" {
#   layer_name = "layer_xarray"
#   s3_bucket  = "cobi-lambda-layers-2023"
#   s3_key     = "layer_xarray.zip"
#   compatible_runtimes = ["python3.8"]
#   description = "Python layer for x86_64 architecture and Python 3.8" 

# }
  
# resource "aws_lambda_layer_version" "layer_motu" {
#   layer_name = "layer_motu"
#   s3_bucket  = "cobi-lambda-layers-2023"
#   s3_key     = "layer_motu.zip"
#   compatible_runtimes = ["python3.8"]
#   description = "Python layer for x86_64 architecture and Python 3.8"

# }

# resource "aws_lambda_layer_version" "layer_numpy" {
#   layer_name = "layer_numpy"
#   s3_bucket  = "cobi-lambda-layers-2023"
#   s3_key = "layer_numpy.zip"
#   compatible_runtimes = ["python3.8"]
#   description = "Python layer for x86_64 architecture and Python 3.8"
  
# }
###

# Lambdas
# resource "aws_lambda_function" "from_csv_to_parquet" {
#   filename      = "./lambda_code/lambda_function.zip"
#   function_name = "from_csv_to_parquet"
#   role          = aws_iam_role.lambda_exec.arn
#   handler       = "lambda_function.lambda_handler"
#   runtime       = "python3.8"
#   layers        = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python38:6",aws_lambda_layer_version.libraries_s3_extras.arn]
#   timeout       = 300
#   memory_size   = 512

#   environment {
#     variables = {
#       INPUT_BUCKET  = ""
#       OUTPUT_BUCKET = ""
#     }
#   }
  
# }



# resource "aws_lambda_function" "copernicus_extract" {
#   filename = copernicus_extract.zip
#   function_name = "copernicus_extract"
#   role = aws_iam_role.lambda_exec.arn
#   handler = "copernicus_extract.lambda_handler"
#   runtime = "python3.8"
# }
