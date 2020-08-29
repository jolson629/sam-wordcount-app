import os
import json
import sys
import boto3


def run_fargate_task(cluster, launchType, subnet_id, taskDefinition, containerName, bucket, inputKey, outputKey, region):
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
                         'name': 'BUCKET',
                         'value': bucket
                     },
                     {
                         'name': 'INPUTKEY',
                         'value': inputKey
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
   
   s3Event = None
   bucket = None
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
         bucket = event['detail']['requestParameters']['bucketName']
         inputKey = event['detail']['requestParameters']['key']
         region = event['detail']['awsRegion']
      except Exception as e:
         error = {'error': 'S3 message missing field bucket, key, or region', 'event':event}
         print(json.dumps(error))
         sys.exit (-1) 

      try:
         #TODO: Figure out a protocol for handeling the output file. Hardwired for now.         
         outputKey = 'out.txt'
         #TODO: Record Fargate execution time in the logs, if AWS doesn't do it for us already...
         msg = {'message':'Start processing', 'event': s3Event, 'cluster': cluster, 'launchType': launchType, 'subnetId': subnetId, 'taskDefinition': taskDefinition, 'containerName': containerName, 'bucket': bucket, 'inputKey': inputKey, 'outputKey': outputKey, 'region': region}
         print(json.dumps(msg))
         response = run_fargate_task(cluster, launchType, subnetId, taskDefinition, containerName, bucket, inputKey, outputKey, region)
         msg = {'message':'Finished processing', 'response': response, 'event': s3Event, 'bucket': bucket, 'inputKey': inputKey, 'outputKey': outputKey, 'region': region}
         print(json.dumps(msg))         
      except Exception as e:
         errorMsg = 'Error launching container on Fargate: %s' %(e)
         error = {'error': errorMsg, 'event': s3Event, 'cluster': cluster, 'launchType': launchType, 'subnetId': subnetId, 'taskDefinition': taskDefinition, 'containerName': containerName, 'bucket': bucket, 'inputKey': inputKey, 'outputKey': outputKey, 'region': region}
         print(json.dumps(error))
         sys.exit (-1) 
            
   else:      
      print('Got S3 event %s. Skipping.' % (s3Event))
      sys.exit (0)
