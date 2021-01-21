import requests
from os import getenv

class SendInBlueMailer:
  def __init__(self):
    self.payload = {
          "sender": {
              "name" : getenv('EMAIL_SUBJECT'),
              "email" : getenv('EMAIL_SENDER')
          },
          "to": [{"email":getenv('EMAIL_TO')}],
          "subject": getenv('EMAIL_SUBJECT'),
      }
    self.headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": getenv('SMTP_API_KEY')
    }

  def send_message(self,message,attachment_url=None):
    # NOTE Don't include Local File
    # Attach link of the file that will be downloaded and sent with mail

    if attachment_url is not None:
      self.payload['attachment']=[{"url": attachment_url}]

    self.payload["textContent"]=message

    response = requests.post(
        getenv('SMTP_API_LINK'),
        json=self.payload, 
        headers=self.headers
      )
    print(response.text)

  def send_html_message(self,html,attachment_url=None):
    # NOTE Don't include Local File
    # Attach link of the file that will be downloaded and sent with mail
    if attachment_url is not None: 
      self.payload['attachment']=[{"url": attachment_url}]
    
    self.payload["htmlContent"]=html
    response = requests.post(
        getenv('SMTP_API_LINK'),
        json=self.payload, 
        headers=self.headers
    )
    print(response.text)