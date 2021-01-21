from util.mail import SendInBlueMailer
from util.s3 import DigitalOceanSpaces
class Notifier:
    def __init__(self):
      self.mail=mail=SendInBlueMailer()
      self.HTML_CONTENT=open('static/html/email-template.html','r').read()
      self.storage=DigitalOceanSpaces()

    def send(self,record):
      report_download_link=self.storage.get_file_link(record['report_file_name'])
      html_content=self.prepare_mail(record)
      self.mail.send_html_message(html_content,report_download_link)
      
    def prepare_mail(self,record):
      html=self.HTML_CONTENT
      html=html\
        .replace("{{crash_id}}",    record["Crash Number"])\
        .replace("{{crash_date}}",  record["Crash Date"].strftime('%m/%d/%Y'))\
        .replace("{{doc_no}}",      record["Document Number"])\
        .replace("{{date_added}}",  record["Add Date"].strftime('%m/%d/%Y'))\
        .replace("{{location}}",    record["Location"])\
        .replace("{{agency}}",      record["Agency"])\
        .replace("{{jurisdiction}}",record["Jurisdiction"])\
        .replace("{{severity}}",    record["Crash Severity"])\
        .replace("{{county}}",      record["County"])

      return html

