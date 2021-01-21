from os import getenv
from scraper import Scraper
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
from dotenv import load_dotenv
load_dotenv()

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
        dsn=getenv('SENTRY_API_LINK'),
        integrations=[sentry_logging],
        traces_sample_rate=1.0,)

scraper=Scraper()
scraper.start_scraping()