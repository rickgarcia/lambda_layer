#!/bin/bash

# Configuration
IMAGE_NAME="lambda-pytorch-transformers-local-pii"
REGION="us-east-1"  # Change to your region
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE_NAME}"
FUNCTION_NAME="lambda-pytorch-transformer-test-pii"

echo "Building and deploying Lambda container image with preloaded model"
echo "----------------------------------------------------------------"

# Ensure all required files exist
echo "Checking for required files..."
for file in Dockerfile requirements.txt lambda_function.py; do
  if [ ! -f "$file" ]; then
    echo "Error: $file not found in current directory"
    exit 1
  fi
done

# 1. Create ECR repository if it doesn't exist
echo "Creating ECR repository if it doesn't exist..."
aws ecr describe-repositories --repository-names "${IMAGE_NAME}" > /dev/null 2>&1 || \
    aws ecr create-repository --repository-name "${IMAGE_NAME}"

# 2. Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region "${REGION}" | \
    docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

# 3. Build Docker image
echo "Building Docker image (this may take several minutes)..."
docker build -t "${IMAGE_NAME}" . | tee build.log

# 4. Tag the image
echo "Tagging image for ECR..."
docker tag "${IMAGE_NAME}:latest" "${ECR_REPO}:latest"

# 5. Push to ECR
echo "Pushing to ECR (this may take several minutes)..."
docker push "${ECR_REPO}:latest" | tee push.log

# 6. Create or update Lambda function
echo "Checking if Lambda function exists..."
if aws lambda get-function --function-name "${FUNCTION_NAME}" > /dev/null 2>&1; then
    echo "Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name "${FUNCTION_NAME}" \
        --image-uri "${ECR_REPO}:latest"
else
    echo "Creating new Lambda function..."
    aws lambda create-function \
        --function-name "${FUNCTION_NAME}" \
        --package-type Image \
        --code ImageUri="${ECR_REPO}:latest" \
        --role "arn:aws:iam::${ACCOUNT_ID}:role/YOUR_LAMBDA_EXECUTION_ROLE" \
        --timeout 60 \
        --memory-size 2048
fi

echo "Done! Lambda function is ready."
echo "You can test it with a sample payload like:"
echo '{
  "body": {
    "text": "The quick brown fox jumps over the lazy"
  }
}'
