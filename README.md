![Alt text](logo.png?raw=true "Zombie Apocalypse")

# Zombie Apocalypse - Addendum #

The purpose of this document is to provide instructions for additional tasks which should be done during Zombie Apocalypse Workshop.

## Lab - Analyzing messages with Athena ##
1. Create a new lambda function, and call it: Zombie_MessageToS3. You can use the IAM Role from previous labs.
2. This time, our lambda function will be created using Python 2.7 environment.
3. Paste the code from scripts/Zombie_MessageToS3.py script.
4. Create a new environment variable. The key is BUCKET_NAME, and the value is the name of your S3 bucket.
5. Increase the execution time of this function to 1 minute.
6. Add new trigger for this function: DynamoDB. Configure it, with your messages table.
7. Wait 1-2 minute, and start writing new messages on your chat window. You should see that flat files are being saved on your S3 bucket with those messages.
8. Open Athena service and execute following script (update the name of your S3 bukcet).

CREATE EXTERNAL TABLE IF NOT EXISTS default.zombie (
  `timestamp` bigint,
  `name` string,
  `message` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://BUCKET_NAME/data/'
TBLPROPERTIES ('has_encrypted_data'='false')

9. Play with the interface and execute some standard S3 queries.

## Lab - Messages to audio ##
1. Create a new IAM role, it should have access to following services: Polly, DynamoDB, CloudWatch, S3, SNS.
2. Create a new lambda function, and call it: "Zombie_MessagesToAudio". Use role which you have created in previous point.
3. Use Python 2.7 environment
4. Paste the code from scripts/Zombie_MessagesToAudio.py script.
5. Create a new environment variable. The key is BUCKET_NAME, and the value is the name of your S3 bucket.
6. Create a new environment variable. The key is USERS_TABLE_NAME, and the value is the name of your DynamoDB table where you store users.
7. Increase the execution time of this function to 1 minute.
8. Add new trigger for this function: DynamoDB. Configure it, with your messages table.
9. Test your application! In the chat window write: "/audio Joanna This is Zombie apocalypse!". You should get a SMS message!
