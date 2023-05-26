resource "aws_s3_bucket_object" "request_layer_object" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "./layers/requests/python.zip"  
  source = "./layers/python.zip"  
}

resource "aws_lambda_layer_version" "libraries_s3_extras" {
  layer_name = "libraries_s3_extras"
  compatible_runtimes = ["python3.8"]
  s3_bucket           = "pro-ed-tech-unete-config"
  s3_key              = "layers/pandas/python.zip"
  
  description         = "Python layer for x86_64 architecture and Python 3.8"
  
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_function" "from_csv_to_parquet" {
  filename      = "./lambda_code/lambda_function.zip"
  function_name = "from_csv_to_parquet"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  layers        = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python38:6",aws_lambda_layer_version.libraries_s3_extras.arn]
  timeout       = 300
  memory_size   = 512

  environment {
    variables = {
      INPUT_BUCKET  = "pro-ed-tech-unete-landing"
      OUTPUT_BUCKET = "pro-ed-tech-unete-staging"
    }
  }

  source_code_hash = filebase64sha256("./lambda_code/lambda_function.zip")

  tracing_config {
    mode = "Active"
  }
}



resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })

  inline_policy {
    name = "lambda_logs_policy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
          Effect   = "Allow"
          Resource = "arn:aws:logs:*:*:*"
        }
      ]
    })
  }
}

resource "aws_iam_policy" "s3_access_policy" {
  name = "s3_access_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::pro-ed-tech-unete-landing",
          "arn:aws:s3:::pro-ed-tech-unete-landing/*",
          "arn:aws:s3:::pro-ed-tech-unete-staging",
          "arn:aws:s3:::pro-ed-tech-unete-staging/*",
          "arn:aws:s3:::pro-ed-tech-unete-raw",
          "arn:aws:s3:::pro-ed-tech-unete-raw/*"
        ]
      }
    ]
  })
}


resource "aws_cloudwatch_log_group" "lambda_logs_request_api" {
  name = "/aws/lambda/request_api_bitacora"
}




#cuando llega algo al bucket se activa la lambda


resource "aws_s3_bucket_notification" "lambda_trigger_raw" {
  bucket = "pro-ed-tech-unete-raw"
  depends_on   = [aws_lambda_permission.s3_invoke_permission_raw]

  lambda_function {
    lambda_function_arn = aws_lambda_function.from_json_to_csv.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = ""
    filter_suffix       = ".json"
  }
}

resource "aws_lambda_permission" "s3_invoke_permission" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.from_csv_to_parquet.arn
  principal     = "s3.amazonaws.com"

  source_account = "719579275730"
  source_arn     = "arn:aws:s3:::pro-ed-tech-unete-landing"
}

resource "aws_lambda_permission" "s3_invoke_permission_raw" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.from_json_to_csv.arn
  principal     = "s3.amazonaws.com"

  source_account = "719579275730"
  source_arn     = "arn:aws:s3:::pro-ed-tech-unete-raw"
}




resource "aws_s3_bucket_object" "directory_2" {
  bucket = "pro-ed-tech-unete-model"
  key    = "DIM/escuelas_dim/"
  acl    = "private"
  content_type = "application/x-directory"
}


resource "aws_s3_bucket_object" "escuela_object" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "./glue_jobs/escuelas_dim.py"  
  source = "./glue_code/escuelas_dim.py"  
}
