#!/bin/bash

# Change the following five lines to deploy...
export APP_NAME=wordcount
export ECR_HOME=543414031934.dkr.ecr.us-east-1.amazonaws.com
export IMAGE_VERSION=0.9.2
export REGION=us-east-1
export CONFIRM_CHANGESET=true

export DEPLOYMENT_NAME=$APP_NAME-deployment


# This is stunningly stupid...
if ! aws s3api head-bucket --bucket "$DEPLOYMENT_NAME" 2>/dev/null; then
   echo Creating S3 bucket $DEPLOYMENT_NAME
   aws s3 mb s3://$DEPLOYMENT_NAME >/dev/null
fi

rm samconfig.toml
cp samconfig_template.toml samconfig.toml

sed -i "s/DEPLOYMENT_NAME/$DEPLOYMENT_NAME/g" samconfig.toml
sed -i "s/APP_NAME/$APP_NAME/g" samconfig.toml
sed -i "s/REGION/$REGION/g" samconfig.toml
sed -i "s/CONFIRM_CHANGESET/$CONFIRM_CHANGESET/g" samconfig.toml
sed -i "s/ECR_HOME/$ECR_HOME/g" samconfig.toml
sed -i "s/IMAGE_VERSION/$IMAGE_VERSION/g" samconfig.toml

sam build
sam deploy -t ./template.yaml 

