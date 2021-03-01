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

        self.CAPTCHA_API_LINK    = getenv('CAPTCHA_API_LINK')
        self.CAPTCHA_STATUS_LINK = getenv('CAPTCHA_API_CHECK_LINK')
        self.CAPTCHA_REPORT_LINK = getenv('CAPTCHA_API_REPORT')
        self.CAPTCHA_API_TOKEN   = getenv('CAPTCHA_API_KEY')

    def solve_normal_captcha(self,base64string):
        self.captchaData['body']=base64string
        self.requests_id=requests.post(
            self.CAPTCHA_API_LINK,
            data=self.captchaData
            ).json()['request']

        print('[.] Captcha Sent to the server')

        while True:
            sleep(4) # Wait for captcha solver service to solve the recaptcha
            captcha_solution=requests.get(
                    self.CAPTCHA_STATUS_LINK\
                        .format(
                            API_KEY=getenv('CAPTCHA_API_KEY'),
                            requests_id=self.requests_id)
                        ).json()['request']

            if captcha_solution != 'CAPCHA_NOT_READY':       
                break
            else:
                print('[=] CAPTCHA NOT READY - Trying again')

        print('[-] Captcha solution Recieved')
        return captcha_solution.upper()

    # [Optional] Report the captcha if that works fine
    def report_good(self):
        self.report('reportgood')

    # Report the captcha if that's wrong
    def report_bad(self):
        self.report('reportbad')

    def report(self,action='reportbad'):
        requests.get(
            self.CAPTCHA_REPORT_LINK.format(
                key=self.CAPTCHA_API_TOKEN,
                action=action,
                report_id=self.requests_id)
        )