#!/bin/bash

# Change the following five lines to deploy...

#export AWS_ACCESS_KEY_ID=$((echo "${1}" | jq .aws_access_key_id ) | tr -d '"' )
#
#export AWS_SECRET_ACCESS_KEY=$((echo "${1}" | jq .aws_secret_access_key) | tr -d '"' )

export APP_NAME=$((echo "${1}" | jq .appname) | tr -d '"' )
echo $1 | jq .appname
echo $APP_NAME
#echo $(echo "${1}" | jq .appname) | tr -d '"'
#echo "APP_NAME: ${APP_NAME}"
#export ECR_HOME=$((echo "${1}" | jq .container) | tr -d '"' )
#export IMAGE_VERSION=$((echo "${1}" | jq .version) | tr -d '"' )
#export CONTAINER_CPU=$((echo "${1}" | jq .cpu) | tr -d '"' )
#echo "CONTAINER_CPU: ${CONTAINER_CPU}"
#export CONTAINER_RAM=$((echo "${1}" | jq .ram) | tr -d '"' )
#
#export REGION=$((echo "${1}" | jq .region) | tr -d '"' )
#echo "REGION: ${REGION}"
#export CONFIRM_CHANGESET=$((echo "${1}" | jq .confirm) | tr -d '"')
