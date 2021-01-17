from os import getenv
import Scraper

from dotenv import load_dotenv
load_dotenv()

mail=SendInBlueMailer(
    API_KEY=getenv('SMTP_API_KEY'),
    TO=getenv('EMAIL_TO'),
)

