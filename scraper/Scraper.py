import requests
from bs4 import BeautifulSoup
from os import getenv
from datetime import datetime, timedelta
from util.captcha import CaptchaSolver
from scraper import Parser
from sentry_sdk import capture_exception, capture_message
import logging

class Scraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.requestHeader={ 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','accept-language': 'en-US,en;q=0.5','user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',}
        
        self.postHeader=self.requestHeader.copy()        
        self.postHeader['Origin']       = getenv('REQUEST_ORIGIN')
        self.postHeader['Referer']      = getenv('REQUEST_REFERER')
        self.postHeader['Content-Type'] = 'application/x-www-form-urlencoded'

        self.COUNTIES={ 48 : 'Lucas', 35 : 'Henry', 26 : 'Fulton', 87 : 'Wood', 62 : 'Ottwa', }
        
        self.date_now=datetime.now()
        
        # ENV is string - So we need to make sure that its converted into int
        PREVIOUS_DAYS=int(getenv('DAYS_BACK'))

        self.start_date = ( self.date_now - timedelta(days=PREVIOUS_DAYS) )\
            .strftime("%m/%d/%Y")\
            .replace('/','%2F')
        self.end_date = self.date_now\
            .strftime("%m/%d/%Y")\
            .replace('/','%2F')

        self.session = requests.Session()
        self.captcha = CaptchaSolver()
        self.parser  = Parser()

    def start_scraping(self):
        for county_id , county_name in self.COUNTIES.items():
            print(f" ===========     {county_name}   =============")
            self.scrape_data_by_county(county_id , county_name)

    def get_search_page_token_and_captcha_answer(self):
        page = self.session.get(
            getenv('REQUEST_LINK_SEARCH_PAGE'), 
            headers=self.requestHeader)

        # TODO Report Error here.
        if page.status_code != 200:
            self.logger.error(
                f' Status code {page.status_code}' ,
                extra={'tags': {'url':page.url,}})

        pageParser = BeautifulSoup(page.content,'html.parser')

        search_page_token = pageParser.find('input',{'name':'__RequestVerificationToken'})['value']
        base64string = pageParser.find('img',class_='captchaImage')['src'].strip().split(',')[1]
    
        captcha_solution = self.captcha.solve_normal_captcha(base64string)

        return search_page_token , captcha_solution

    def scrape_data_by_county(self,county_code,county_name):
        # A flag to try atleast 2 times
        first_try=True
        while True:
            # Each requests to begin will require a token and captcha solution
            search_page_token , captcha_solution = self.get_search_page_token_and_captcha_answer()

            # Completing data to be sent to the server for POST request
            DATA1=getenv('REQUEST_DATA_POST_1')\
                    .format(
                        token=search_page_token,
                        start_date=self.start_date,
                        end_date=self.end_date,
                        county=county_code,
                        captcha=captcha_solution
                        )
            
            print('Sending POST Requests')
            # Initiate the searching process
            resultPage=self.session.post(
                getenv('REQUEST_LINK_POST_1'),
                headers=self.postHeader,
                data=DATA1)

            # TODO report to sentry for error Handling
            if resultPage.status_code!=200:
                self.logger.error(
                    f'[{resultPage.status_code}] - {resultPage.url}' ,
                    extra={'tags': {'url':resultPage.url,'status':resultPage.status_code}})

            resultPageParser=BeautifulSoup(resultPage.content,'html.parser')

            token=self.parser.get_verification_token(resultPageParser)

            # TODO Report to Sentry for Error
            try:
                self.parser.parse_result( resultPageParser , county_name , self.session)
                break # If upper code work fine break the loop
            
            except ValueError as err:
                capture_exception(err)
                # capture_message(f'[X] ERROR Happened {captcha_solution} - {county_name}')

                self.logger.error(
                    f'Wrong Captcha' ,
                    extra={'tags': {
                        'county':county_name,
                        'captcha-solution':captcha_solution,
                        'stage':'scrape_data_by_county',
                        }})

                # print('[X] ERROR Happened', captcha_solution , county_name)
                self.captcha.report_bad()
                
                # Try one more time to test if we can get the data
                if first_try:
                    print('Trying Again')
                    first_try=False
                    continue
                else:
                    break
            break # Just for a safer side
        

        # Moving to next page
        if self.parser.is_next_button_exists(resultPageParser):
            for page_no in range(1,20):
                print("Page : ",page_no)
                DATA2=getenv('REQUEST_DATA_POST_2')\
                        .format(
                            token=token,
                            start_date=self.start_date,
                            end_date=self.end_date,
                            county=county_code,
                            captcha=captcha_solution,
                            page_no=page_no,
                        )

                resultPage=self.session.post(
                            getenv('REQUEST_LINK_POST_2'),
                            headers=self.postHeader,
                            data=DATA2
                        )

                # TODO report error to Sentry
                if resultPage.status_code != 200: 
                    print('[!] Page status code: ',resultPage.status_code)

                resultPageParser=BeautifulSoup(resultPage.content,'html.parser')

                token=self.parser.get_verification_token(resultPageParser)

                self.parser.parse_result(resultPageParser , county_name, self.session)
                
                if self.parser.is_next_button_exists(resultPageParser):
                    # Next Button can be seen keep working
                    continue
                else:
                    # Next Button is disappeared - Stop the bot here.
                    break