import boto3
from os import getenv
class DigitalOceanSpaces:
    def __init__(self):
        s3config = {
            "region_name":          getenv('DO_OBJECT_STORAGE_REGION'),
            "endpoint_url":         "https://{}.digitaloceanspaces.com".format(getenv('DO_OBJECT_STORAGE_REGION')),
            "aws_access_key_id":    getenv('DO_OBJECT_STORAGE_KEY'),
            "aws_secret_access_key":getenv('DO_OBJECT_STORAGE_SECRET') 
        }
        self.BUCKET             = getenv('DO_BUCKET')
        self.DO_FOLDER          = getenv('DO_FOLDER')
        self.EXPIRATION_SECONDS = int(getenv('DO_FILE_EXPIRATION_SECONDS'))

        self.s3client = boto3.client("s3", **s3config)
        self.s3resource = boto3.resource("s3", **s3config)

        self.set_of_uploaded_reports=set(
            [x.key.replace(self.DO_FOLDER+'/','') for x in s3resource.Bucket('state-car-reports').objects.all()]
        )


    def upload_file(self, file_to_upload, name_after_upload):
        response=self.s3client.upload_file(
            file_to_upload,
            self.BUCKET,
            f"{self.DO_FOLDER}/{name_after_upload}"
        )
    
    def if_file_exists(self, report_file_name):
        return report_file_name in self.set_of_uploaded_reports

    def get_file_link(self, uploaded_file_name):
        download_link=self.s3client\
            .generate_presigned_url('get_object',
                Params={'Bucket': self.BUCKET,
                        'Key': f"{self.DO_FOLDER}/{uploaded_file_name}"},
                ExpiresIn=self.EXPIRATION_SECONDS)
        
        return download_link
        # TODO Add exception handling here with sentry



        