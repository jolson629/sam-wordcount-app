#!/bin/bash

export CLUSTER=sam-wordcount-app-cluster
export LAUNCH_TYPE=FARGATE
export TASK_DEFINITION=sam-wordcount-app
export SUBNET_ID=subnet-0699a874e7024ec07
export CONTAINER_NAME=wordcount

aws lambda invoke \
   --function-name "EventConsumerFunction" \
   --endpoint-url "http://127.0.0.1:3001" \
   --no-verify-ssl \
   --payload '{"version": "0", "id": "1a368b7a-8324-5c29-d342-e036fef5fd7a", "detail-type": "AWS API Call via CloudTrail", "source": "aws.s3", "account": "543414031934", "time": "2020-08-25T21:09:51Z", "region": "us-east-1", "resources": [], "detail": {"eventVersion": "1.07", "userIdentity": {"type": "IAMUser", "principalId": "AIDAX5BQACY7OGSBJUZ4Y", "arn": "arn:aws:iam::543414031934:user/s3upload", "accountId": "543414031934", "accessKeyId": "AKIAX5BQACY7ERHR3GOH", "userName": "s3upload"}, "eventTime": "2020-08-25T21:09:51Z", "eventSource": "s3.amazonaws.com", "eventName": "PutObject", "awsRegion": "us-east-1", "sourceIPAddress": "73.247.96.55", "userAgent": "[aws-cli/1.17.14 Python/3.8.2 Linux/5.4.0-42-generic botocore/1.14.14]", "requestParameters": {"bucketName": "sam-wordcount-app-src", "Host": "sam-wordcount-app-src.s3.amazonaws.com", "key": "input.txt"}, "responseElements": "None", "additionalEventData": {"SignatureVersion": "SigV4", "CipherSuite": "ECDHE-RSA-AES128-GCM-SHA256", "bytesTransferredIn": 2143.0, "AuthenticationMethod": "AuthHeader", "x-amz-id-2": "UrPOYoWe5hmc8t2jJaQwG0+YyKlFZM8E7jFVAypEBfBIKLAaBE867Gic+RKyBmPASJS2Wpshoeg=", "bytesTransferredOut": 0.0}, "requestID": "600315AE0BA340CF", "eventID": "842774f4-dd9f-46f5-8280-ebc3980b9d3b", "readOnly": "False", "resources": [{"type": "AWS::S3::Object", "ARN": "arn:aws:s3:::s3-eventbridge-src-bucket-jjo/README.md"}, {"accountId": "543414031934", "type": "AWS::S3::Bucket", "ARN": "arn:aws:s3:::s3-eventbridge-src-bucket-jjo"}], "eventType": "AwsApiCall", "managementEvent": "False", "recipientAccountId": "543414031934", "eventCategory": "Data"}}' \
   out.txt
