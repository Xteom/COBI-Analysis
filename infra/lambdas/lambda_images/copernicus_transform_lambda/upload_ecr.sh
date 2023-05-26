img_name='copernicus_transform_lambda'
aws_region='us-east-2'
aws_account_id='395849996067'


# Update and build docker image

#print current working directory
echo "Building docker image..."
docker build -t $img_name .
echo "Docker image built"
docker tag $img_name $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$img_name
echo "Docker image tagged"
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

# Push docker image to ECR
docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$img_name
