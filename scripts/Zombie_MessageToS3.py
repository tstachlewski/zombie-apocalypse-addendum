import os
import uuid
import boto3

def lambda_handler(event, context):

    print 'Creating new flat files on S3 based on DynamoDB records'

    records = event['Records']

    id = str(uuid.uuid4())

    output = os.path.join("/tmp/", id + ".txt")
    with open(output, "a") as file:
        for record in records:

            print record

            timestamp =  record['dynamodb']['NewImage']['timestamp']['N']
            message = record['dynamodb']['NewImage']['message']['S']
            name = record['dynamodb']['NewImage']['name']['S']

            print timestamp + "," + name + "," + message

            file.write(timestamp + "," + name + "," + message )


    s3 = boto3.client('s3')
    s3.upload_file("/tmp/" + id + ".txt", os.environ['BUCKET_NAME'], "data/" + id + ".txt")

    print 'Success'
