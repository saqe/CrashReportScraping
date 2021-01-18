from os import getenv
import sentry_sdk
from flask import Flask

from scraper import Scraper

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

sentry_sdk.init(
    getenv('SENTRY_API_LINK'),
    traces_sample_rate=1.0
)

@app.route('/start-the-scraper')
def hello_name():
    scraper=Scraper()
    scraper.start_scraping()
    return 'Started'

@app.route('/')
def wellcome():
   return 'Hello world'

if __name__ == '__main__':
   app.run(debug = True)





