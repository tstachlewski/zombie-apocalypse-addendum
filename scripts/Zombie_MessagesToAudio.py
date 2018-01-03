import boto3
import uuid
import os
from contextlib import closing

def lambda_handler(event, context):

    timestamp = event['Records'][0]['dynamodb']['NewImage']['timestamp']['N']
    message = event['Records'][0]['dynamodb']['NewImage']['message']['S']

    if message.startswith("/audio"):
        voice = message[7:].split(" ", 1)[0]
        message = message[7:].split(" ", 1)[1]

        print message
        print voice

        # Using Amazon Polly service to convert text to speech
        polly = boto3.client('polly')
        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text=message,
            TextType='text',
            VoiceId=voice
        )

        # Save audio on local directory
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join("/tmp/", timestamp)
                with open(output, "a") as file:
                    file.write(stream.read())

        # Save audio file on S3
        newKey = "audio/" + str(timestamp) + ".mp3"
        s3 = boto3.client('s3')
        s3.upload_file('/tmp/' + timestamp, os.environ['BUCKET_NAME'], newKey)
        s3.put_object_acl(ACL='public-read', Bucket=os.environ['BUCKET_NAME'], Key= newKey)

        location = s3.get_bucket_location(Bucket=os.environ['BUCKET_NAME'])
        region = location['LocationConstraint']

        if region is None:
            url_begining = "https://s3.amazonaws.com/"
        else:
            url_begining = "https://s3-" + str(region) + ".amazonaws.com/" \

        url = url_begining \
                + str(os.environ['BUCKET_NAME']) \
                + "/audio/" \
                + timestamp \
                + ".mp3"


        dynamodb = boto3.client('dynamodb')
        response = dynamodb.scan(TableName = str(os.environ['USERS_TABLE_NAME']))

        sns = boto3.client('sns')
        for user in response['Items']:
            phone = user['phone']['S']
            print 'Sending sms (' + url + ') to: ' + phone
            sns.publish(
                Message = url,
                PhoneNumber = phone
            )



    return 'Success'
