from os import getenv
import sentry_sdk

from scraper import Scraper

from dotenv import load_dotenv
load_dotenv()

sentry_sdk.init(
    getenv('SENTRY_API_LINK'),
    traces_sample_rate=1.0
)

scraper=Scraper()
scraper.start_scraping()
