import boto3
from os import getenv

class DigitalOceanSpaces:
    def __init__(self):
        s3config = {
            "region_name": getenv('DO_OBJECT_STORAGE_REGION'),
            "endpoint_url": "https://{}.digitaloceanspaces.com".format(getenv('DO_OBJECT_STORAGE_REGION')),
            "aws_access_key_id": getenv('DO_OBJECT_STORAGE_KEY'),
            "aws_secret_access_key": getenv('DO_OBJECT_STORAGE_SECRET') 
        }
        
        self.s3client = boto3.client("s3", **s3config)

    def upload_file(self, file_to_upload, name_after_upload):
        response=self.s3client.upload_file(
            file_to_upload,
            getenv('DO_BUCKET'),
            f"{getenv('DO_FOLDER')}/{name_after_upload}"
        )
    
    def get_file_link(self, uploaded_file_name):
        download_link=self.s3client\
            .generate_presigned_url('get_object',
                Params={'Bucket': getenv('DO_BUCKET'),
                        'Key': f"{getenv('DO_FOLDER')}/{uploaded_file_name}"},
                ExpiresIn=int(getenv('DO_FILE_EXPIRATION_SECONDS')))
        
        return download_link
        # TODO Add exception handling here with sentry



        