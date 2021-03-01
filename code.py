# from util import mail
from dotenv import load_dotenv
load_dotenv()

import logging
import boto3
from os import getenv

s3config = {
      "region_name": getenv("DO_OBJECT_STORAGE_REGION"),
      "endpoint_url": "https://{}.digitaloceanspaces.com".format(getenv('DO_OBJECT_STORAGE_REGION')),
      "aws_access_key_id": getenv('DO_OBJECT_STORAGE_KEY'),
      "aws_secret_access_key": getenv('DO_OBJECT_STORAGE_SECRET') 
  }

# Initializing S3.ServiceResource object - http://boto3.readthedocs.io/en/latest/reference/services/s3.html#service-resource
s3resource = boto3.resource("s3", **s3config)

# Initializing S3.Client object - http://boto3.readthedocs.io/en/latest/reference/services/s3.html#client
s3client = boto3.client("s3", **s3config)
s3client = boto3.client("s3", **s3config)
import os
print('====',os.path.dirname(__file__))
print('====',os.getcwd()) 