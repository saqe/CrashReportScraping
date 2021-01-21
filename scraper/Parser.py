from util.db import DatabaseManager
from sentry_sdk import capture_exception, capture_message
from datetime import datetime
import requests
from os import getenv
from util.notifier import Notifier
from util.filemanager import FileManager
class Parser:
    def __init__(self):
        self.db=DatabaseManager()
        self.notify=Notifier()
        self.filemanager=FileManager()

    def get_verification_token(self, pageParser):
        return pageParser\
            .find('form',{'id':'Search'})\
            .find('input',{'name':'__RequestVerificationToken'})['value']

    def is_next_button_exists(self, pageParser):
        return pageParser.find('li',{'aria-label':'Next page'}) is not None

    def get_pdf_reports(self, first_btn, record, session):
        crash_number=record['Crash Number']
        btn_id=first_btn.find('input', {'name':'id'})['value']
        btn=first_btn.find('button', {'type':'submit'})['id']
        request_verification=first_btn.find('input', {'name':'__RequestVerificationToken'})['value']
            
        page=session.post(
            getenv('REQUEST_LINK_REPORT') +'/GetReport',
            data=f'__RequestVerificationToken={request_verification}&id={btn_id}&{btn}=' ,
            headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                'Content-Type':'application/x-www-form-urlencoded',
                'Referer': getenv('REQUEST_LINK_REPORT')+ '/Search',
                }
            )
        
        self.filemanager.download_pdf_report_local(page, record['report_file_name'])


    def parse_result(self, pageParser, county_name, session):
        # TODO report error here with Sentry
        if pageParser.find('h2',{'aria-label':'Error Message'}) is not None:
            capture_message('Error reported at parse result - error message shown')
        
        # TODO Report an error here with Sentry
        if pageParser.h1.text != "Crash Results":
            print('[x] There is an error occured')
            raise ValueError

        results=pageParser.find('table',{'id':'mySearchTable'}).findAll('tr', 'selectable')

        for row in results:
            fields = row.findAll('td')
            result = [field.text.strip() for field in fields[1:]]

            # Map all of the Fields data with with headers and make them a dictoinary
            record = dict(
                        zip(
                            ['Crash Number', 'Crash Date', 'Add Date', 'Location', 'Agency', 'Jurisdiction', 'Crash Severity', 'Document Number'],
                            result
                        )
                    )
            
            # Convert all of the string dates in datetime stamp for accessibility in database searching
            record['Scraped_date']=  datetime.now()
            record['Add Date']   = datetime.strptime( record['Add Date']  , '%m/%d/%Y')
            record['Crash Date'] = datetime.strptime( record['Crash Date'], '%m/%d/%Y')

            record['County'] = county_name
            record['report_file_name']=f"{record['Crash Number']}.pdf"

            # If record already exists - Don't save that in data
            if self.db.ifIndexExists(record['Crash Number']) : 
                return
            
            # Download PDF report copy of the crash.
            self.get_pdf_reports(fields[0], record, session)
            
            # NOTE a directory can be added here for local file
            self.filemanager.upload_report_on_cloud(
                file_to_upload      = record['report_file_name'],
                name_after_upload   = record['report_file_name']
                )

            # Send an Email / Slack Notification to Person
            self.notify.send(record)

            # Record is new will be added in Database
            self.db.insert_record(record)

            # After Processing and Uploading of report to Storage. Delete a local copy of report
            self.filemanager.delete_local_pdf_report(record['report_file_name'])

            # TODO Sentry record it
            # Transaction

