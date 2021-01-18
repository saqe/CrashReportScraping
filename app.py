from os import getenv
from flask import Flask, request
from scraper import Scraper
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/start-the-scraper')
def hello_name():
    if request.args.get('token')==getenv('TOKEN'):
        scraper=Scraper()
        scraper.start_scraping()
        return 'Started'
    else:
        return 'You might be lost'

@app.route('/')
def wellcome():
    return 'Hello world'

if __name__ == '__main__':
    sentry_sdk.init(
        dsn=getenv('SENTRY_API_LINK'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,)

    # Certifacte for Heroku
    with open(getenv('MONGODB_CON_CERT_FILE'), "w") as cert:
        cert.write(getenv('CERT'))
    app.run()