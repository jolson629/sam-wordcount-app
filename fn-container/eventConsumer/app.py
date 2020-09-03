import os
import json
import sys
import boto3


def run_fargate_task(cluster, launchType, subnet_id, taskDefinition, containerName, inputBucket, inputKey, outputBucket, outputKey, region):
   client = boto3.client('ecs', region_name=region)
   response = client.run_task(    
      cluster = cluster,
      launchType = launchType,
      taskDefinition = taskDefinition,
      count = 1,
      platformVersion='LATEST',
           networkConfiguration={
               'awsvpcConfiguration': {
                   'subnets': [
                       subnet_id,
                   ],
                   'assignPublicIp': 'DISABLED'
               }
        },
      overrides={
         'containerOverrides': [
             {
                 'name': containerName,
                 'environment': [
                     {
                         'name': 'REGION',
                         'value': region
                     },
                     {
                         'name': 'INPUTBUCKET',
                         'value': inputBucket
                     },
                     {
                         'name': 'INPUTKEY',
                         'value': inputKey
                     },
                     {
                         'name': 'OUTPUTBUCKET',
                         'value': outputBucket
                     },
                     
                     {
                         'name': 'OUTPUTKEY',
                         'value': outputKey
                     }
                 ],
             },
         ],
      }
   )
   return str(response)

def lambda_handler(event, context):
   #TODO: Since this is invoked by EventBridge, are sys.exit(-1) and sys.exit(0) clean fail exits?
   
   #TODO: Collapse all parameters into a dictionary.
   #TODO: Environment variables into Lambda. Do these get passed in when the lambda is executed locally, or are they None?   
   
   cluster = os.environ["CLUSTER"]
   launchType = os.environ["LAUNCH_TYPE"]
   taskDefinition = os.environ["TASK_DEFINITION"]
   subnetId = os.environ["SUBNET_ID"]
   containerName = os.environ["CONTAINER_NAME"]
   outputBucket = os.environ["OUTPUT_BUCKET"]
   
   error = None
   if (cluster == None):
      error = {'error': 'Required environment variable CLUSTER is not defined.'}
   if (launchType == None):
      error = {'error': 'Required environment variable LAUNCH_TYPE is not defined.'}
   if (taskDefinition == None):
      error = {'error': 'Required environment variable TASK_DEFINITION is not defined.'}
   if (subnetId == None):
      error = {'error': 'Required environment variable SUBNET_ID is not defined.'}
   if (containerName == None):
      error = {'error': 'Required environment variable CONTAINER_NAME is not defined.'}
   if (outputBucket == None):
      error = {'error': 'Required environment variable OUTPUT_BUCKET is not defined.'}

   if error is not None:
      print(json.dumps(error))      
      sys.exit (-1)
         
   s3Event = None
   inputBucket = None
   inputKey = None
   region = None
   try:
      s3Event = event['detail']['eventName']
   except Exception as e:
      error = {'error': 'S3 message malformed or missing field ["detail"]["eventName"]', 'event':event}
      print(json.dumps(error))
      sys.exit (-1)

   if s3Event == 'PutObject':
      try:
         inputBucket = event['detail']['requestParameters']['bucketName']
         inputKey = event['detail']['requestParameters']['key']
         region = event['detail']['awsRegion']
      except Exception as e:
         error = {'error': 'S3 message missing field inputBucket, key, or region', 'event':event}
         print(json.dumps(error))
         sys.exit (-1) 

      try:
         outputKey = inputKey+'.out'
         msg = {'message':'Start processing', 'event': s3Event, 'cluster': cluster, 'launchType': launchType, 'subnetId': subnetId, 'taskDefinition': taskDefinition, 'containerName': containerName, 'inputBucket': inputBucket, 'inputKey': inputKey, 'outputBucket':outputBucket, 'outputKey': outputKey, 'region': region}
         print(json.dumps(msg))
         response = run_fargate_task(cluster, launchType, subnetId, taskDefinition, containerName, inputBucket, inputKey, outputBucket, outputKey, region)
         msg = {'message':'Finished processing', 'response': response, 'event': s3Event, 'inputBucket': inputBucket, 'inputKey': inputKey, 'outputBucket': outputBucket, 'outputKey': outputKey, 'region': region}
         print(json.dumps(msg))         
      except Exception as e:
         errorMsg = 'Error launching container on Fargate: %s' %(e)
         error = {'error': errorMsg, 'event': s3Event, 'cluster': cluster, 'launchType': launchType, 'subnetId': subnetId, 'taskDefinition': taskDefinition, 'containerName': containerName, 'inputBucket': inputBucket, 'inputKey': inputKey, 'outputBucket': outputBucket, 'outputKey': outputKey, 'region': region}
         print(json.dumps(error))
         sys.exit (-1) 
            
   else:      
      print('Got S3 event %s. Skipping.' % (s3Event))
      sys.exit (0)
