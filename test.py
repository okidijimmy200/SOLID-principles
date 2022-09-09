data = open('test.json', 'rb')
import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')
s3.Bucket('image-store-1995').put_object(Key='test.json', Body=data)