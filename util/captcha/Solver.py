import requests
from os import getenv
from time import sleep
from sentry_sdk import capture_exception, capture_message

class CaptchaSolver:
    def __init__(self):
        self.captchaData={
            'method'  :'base64',
            'key'     :getenv('CAPTCHA_API_KEY'),
            'json'    :1,
            'caseSensitive':1,
        }

    def solve_normal_captcha(self,base64string):
        self.captchaData['body']=base64string
        self.requests_id=requests.post(
            getenv('CAPTCHA_API_LINK'),
            data=self.captchaData
            ).json()['request']

        print('Captcha Sent to the server')
            
        while True:
            sleep(4) # Wait for captcha solver service to solve the recaptcha
            captcha_solution=requests.get(
                    getenv('CAPTCHA_API_CHECK_LINK')\
                        .format(
                            API_KEY=getenv('CAPTCHA_API_KEY'),
                            requests_id=self.requests_id)
                        ).json()['request']

            if captcha_solution != 'CAPCHA_NOT_READY':       
                break
            else:
                # capture_message('CAPTCHA NOT READY - Trying again')
                print('CAPTCHA NOT READY - Trying again')

        print('[-] Captcha Solved')
        
        capture_message(f'Recaptcha ID : {self.requests_id}  | Solution : {captcha_solution.upper()}')
        return captcha_solution.upper()

    # [Optional] Report the captcha if that works fine
    def report_good(self):
        requests.get(
            getenv('CAPTCHA_API_REPORT').format(
                key=getenv('CAPTCHA_API_KEY'),
                action='reportgood',
                report_id=self.requests_id)
        )

    # Report the captcha if that's wrong
    def report_bad(self):
        
        # capture_message(f'[Report BAD] Request ID : {self.requests_id} ')
        requests.get(
            getenv('CAPTCHA_API_REPORT').format(
                key=getenv('CAPTCHA_API_KEY'),
                action='reportbad',
                report_id=self.requests_id)
        )
        