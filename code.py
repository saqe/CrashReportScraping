from util import SendInBlueMailer
from os import getenv

from dotenv import load_dotenv
load_dotenv()

mail=SendInBlueMailer(
    API_KEY=getenv('SMTP_API_KEY'),
    TO=getenv('EMAIL_TO'),
)

