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