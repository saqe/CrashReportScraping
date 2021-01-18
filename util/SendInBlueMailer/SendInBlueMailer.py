import requests
from os import getenv

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

def send_message(self,message):
  self.payload["textContent"]=message

  response = requests.post(
      getenv('SMTP_API_LINK'),
      json=self.payload, 
      headers=self.headers
    )
  print(response.text)
  