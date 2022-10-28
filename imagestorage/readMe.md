ImageStorage:
Designed a interface to our ImageStorage system that performs operations of upload,
download, getFileURL, delete operations.
Created an AWS implementation of interface called AWSStorage that is connected to an AWS s3 bucket to perform 
operation on image.
Also implemented minio implementation of interface called Minio that is connected to Minio s3 bucket.

Created a Image Storage system that implements the interfaces injected into it through dependency injection
so we can choose either minio or aws implementation of interface.

Performed unittests for the system.