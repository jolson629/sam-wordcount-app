import os
import json
import sys
import boto3

def lambda_handler(event, context):

   s3Event = None
   bucket = None
   key = None
   region = None
   try:
      s3Event = event['detail']['eventName']
   except Exception as e:
      error = {'error': 'S3 message malformed or missing field ["detail"]["eventName"]', 'event':event}
      print(json.dumps(error))
      sys.exit (-1)

   if s3Event == 'PutObject':
      try:
         bucket = event['detail']['requestParameters']['bucketName']
         key = event['detail']['requestParameters']['key']
         region = event['detail']['awsRegion']
         print('Processing event %s on %s/%s (%s)' % (s3Event, bucket, key, region))
      except Exception as e:
         error = {'error': 'S3 message missing field bucket, key, or region', 'event':event}
         print(json.dumps(error))
         sys.exit (-1) 
   else:      
      print('Got S3 event %s. Skipping.' % (s3Event))
      sys.exit (0)
