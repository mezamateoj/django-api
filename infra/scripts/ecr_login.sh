#!/bin/bash

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Get default region or use provided region
AWS_REGION=${AWS_REGION:-us-east-1}

echo "Logging into ECR in account ${AWS_ACCOUNT_ID} region ${AWS_REGION} ..."

# Get ECR login token and execute docker login
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

if [ $? -eq 0 ]; then
    echo "Successfully logged into ECR"
else
    echo "Failed to log into ECR"
    exit 1
fi 