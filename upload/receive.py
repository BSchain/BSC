import boto3

# Create SQS client
sqs = boto3.client('sqs')


queue_url = 'https://cn-north-1.queue.amazonaws.com.cn/444376591338/test'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)
message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']

# Delete received message from queue
sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)
#print('Received and deleted message: %s' % message)
print('Received and deleted message: %s' % message)
print(message['MessageAttributes']['Author'])
