#get current working directory
current_dir=$(pwd)

#upload the lambda images to ECR
cd ./lambdas/lambda_images/copernicus_extract_lambda && sh upload_ecr.sh
cd ../copernicus_transform_lambda && sh upload_ecr.sh
cd $current_dir

echo "Lambda images uploaded to ECR"