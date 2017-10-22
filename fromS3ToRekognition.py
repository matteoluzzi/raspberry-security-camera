import boto3
import json

def lambda_handler(event, context):
    print json.dumps(event)

    rekonClient = boto3.client('rekognition')

    for record in event["Records"]:

        eventName = record["eventName"]
        if not eventName == "ObjectCreated:Put":
            print "Unrecognised event type " + eventName
        else:
            bucket = record["s3"]["bucket"]["name"]
            objectKey = record["s3"]["object"]["key"]

            image = dict()
            s3Obj = dict()

            s3Obj["Bucket"] = bucket
            s3Obj["Name"] = objectKey
            image["S3Object"] = s3Obj

            response = rekonClient.detect_labels(Image=image)

            print response
