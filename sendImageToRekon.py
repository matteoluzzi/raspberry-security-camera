import boto3
import json

def lambda_handler(event, context):
    print json.dumps(event)

    rekonClient = boto3.client('rekognition')

    bucket = event["bucketName"]
    objectKey = event["s3Key"]

    image = dict()
    s3Obj = dict()

    s3Obj["Bucket"] = bucket
    s3Obj["Name"] = objectKey
    image["S3Object"] = s3Obj

    response = rekonClient.detect_labels(Image=image)

    return json.dumps(response["Labels"])
