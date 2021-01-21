from os import remove
from util.s3 import DigitalOceanSpaces
from sfrom sentry_sdk import capture_exception
class FileManager:
    def __init__(self):
      self.storage=DigitalOceanSpaces()

    def upload_report_on_cloud(self, file_to_upload, name_after_upload):
        # TODO Just for testing
        if self.storage.if_file_exists(file_to_upload):return 

        self.storage.upload_file(file_to_upload, name_after_upload)
    
    def download_pdf_report_local(self, page, report_file_name):
        # TODO Just for testing
        if self.storage.if_file_exists(report_file_name):return 
        
        if page.headers['Content-Type']=='application/pdf':
            with open(report_file_name, 'wb') as f:
                f.write(page.content)
                print("PDF report Downloaded")
        else:
            print("Something went wrong")

    def delete_local_pdf_report(self, report_file_name):
        # File copy will be deleted from server storage permanentely.
        try:
            remove(report_file_name)
        except FileNotFoundError as err:
            capture_exception(err)

            # asdaa
            git config --global user.email "saqib.py@gmail.com"
            git config --global user.name "Saqib"