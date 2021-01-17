import requests as re
from bs4 import BeautifulSoup
from os import getenv
from datetime import datetime, timedelta
from catpchaSolver import Solver

class Scraper:
    def __init__(self, name, age):
        self.requestHeader={ 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','accept-language': 'en-US,en;q=0.5','cache-control': 'no-cache','pragma': 'no-cache','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',}
        
        self.postHeader=self.requestHeader.copy()        
        self.postHeader['Origin']       = getenv('REQUEST_ORIGIN')
        self.postHeader['Referer']      = getenv('REQUEST_REFERER')
        self.postHeader['Content-Type'] = 'application/x-www-form-urlencoded'

        self.COUNTIES={ 48 : 'Lucas', 35 : 'Henry', 26 : 'Fulton', 87 : 'Wood', 62 : 'Ottwa', }
        
        self.date_now=datetime.now()
        self.start_date = ( date_now - timedelta(days=3) )\
            .strftime("%m/%d/%Y")\
            .replace('/','%2F')
        self.end_date = date_now\
            .strftime("%m/%d/%Y")\
            .replace('/','%2F')

        self.session=requests.Session()

        self.captcha=Solver()

    def start_scraping(self):
        for county_id , county_name in self.COUNTIES.items():
            self.scrape_data_by_county(county_id , county_name)

    def get_search_page_token_and_captcha_answer(self):
        page = self.session.get(
            getenv('REQUEST_LINK_SEARCH_PAGE'), 
            headers=self.requestHeader)

        # TODO Report Error here.
        if page.status_code != 200: 
            print('[!] Page status code: ' , page.status_code)

        pageParser = BeautifulSoup(page.content,'html.parser')

        search_page_token = pageParser.find('input',{'name':'__RequestVerificationToken'})['value']
        base64string = pageParser.find('img',class_='captchaImage')['src'].strip().split(',')[1]
    
        captcha_solution = self.captcha.solve_normal_captcha(base64string)

        return search_page_token , captcha_solution

    def scrape_data_by_county(self,county_code,county_name):
        # Each requests to begin will require a token and captcha solution
        search_page_token , captcha_solution = self.get_search_page_token_and_captcha_answer(self)

        # Completing data to be sent to the server for POST request
        DATA1=getenv('REQUEST_DATA_POST_1')\
                .format(
                    token=search_page_token,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    county=county_code,
                    captcha=captcha_solution
                    )
        
        # Initiate the searching process
        resultPage=self.session.post(
            getenv('REQUEST_LINK_POST_1'),
            headers=self.postHeader,
            data=DATA1)

        # TODO report to sentry for error Handling
        if resultPage.status_code!=200: 
            print('[!] Page status code: ',resultPage.status_code)
        
        resultPageParser=BeautifulSoup(resultPage.content,'html.parser')

        self.token=resultPageParser.find('form',{'id':'Search'}).find('input',{'name':'__RequestVerificationToken'})['value']

        # TODO Report to Sentry for Error

        try:    
            parse_result( resultPageParser , county_name)
        except: 
            print ('[X] ERROR Happened', captcha , county_name)


        # Moving to next page
        if resultPageParser.find( 'li' , {'aria-label':'Next page'} ) is not None:
            for page_no in range(1,20):
                print("Page : ",page_no)
                DATA2=getenv('REQUEST_DATA_POST_2')\
                        .format(
                            token=self.token,
                            start_date=self.start_date,
                            end_date=self.end_date,
                            county=county_code,
                            captcha=captcha_solution,
                            page_no=page_no,
                        )

                resultPage=self.session.post(
                    getenv('REQUEST_LINK_POST_2'),
                    headers=self.postHeader,
                    data=DATA2)

                # TODO report error to Sentry
                if resultPage.status_code != 200: 
                    print('[!] Page status code: ',resultPage.status_code)

                resultPageParser=BeautifulSoup(resultPage.content,'html.parser')

                self.token=resultPageParser\
                    .find('form',{'id':'Search'})\
                    .find('input',{'name':'__RequestVerificationToken'})['value']
                
                scrape_result(resultPageParser , county_name)
                
                if resultPageParser\
                    .find('li',{'aria-label':'Next page'}) is None:
                    # Next Button is disappeared - Stop the bot here.
                    break
                else:
                    # Next Button can be seen keep working
                    continue


        
            
        
        

        
        
