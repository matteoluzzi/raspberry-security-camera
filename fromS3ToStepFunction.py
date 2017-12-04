import boto3
import json
import os

stepfunctionsArn = os.getenv("STEP_FUNCTION_ARN", "")

def lambda_handler(event, context):

    print 'S3 event: ' + json.dumps(event)

    for record in event["Records"]:
        eventName = record["eventName"]
        if not eventName == "ObjectCreated:Put":
            print "Unrecognised event type " + eventName
        else:
            s3ObjectKey = record["s3"]["object"]["key"]
            bucketArn = record["s3"]["bucket"]["arn"]
            bucketName = record["s3"]["bucket"]["name"]

            inputParams = dict()
            inputParams["s3Key"] = s3ObjectKey
            inputParams["bucketName"] = bucketName
            inputParams["bucketArn"] = bucketArn

            stepFunctionsClient = boto3.client('stepfunctions')

            response = stepFunctionsClient.start_execution(
                stateMachineArn=stepfunctionsArn,
                name=s3ObjectKey,
                input=json.dumps(inputParams)
            )

            print 'Started execution of step functions: arn ' + response["executionArn"] + ', execution date: ' + str(response["startDate"])
