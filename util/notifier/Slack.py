import requests
from os import getenv

class SlackHook:
    def __init__(self):
        self.HOOK_LINK=getenv('SLACK_HOOK') 
        self.POST_DATA={
            "blocks": [{
                "type": "section",
                "fields": []
            }]
        }

    def set_hook(self, hook):
        self.HOOK_LINK=hook

    def send_text(self, message):
        requests.post(
            self.HOOK_LINK,
            headers={'Content-type':'application/json'},
            json={"text":message},
        ).text

    def send_custom(self, payload):
        requests.post(
            self.HOOK_LINK,
            headers={'Content-type':'application/json'},
            json=payload
        ).text

    def send_dict_attributes(self, dataDict):
        fields=[]
        payload=self.POST_DATA.copy()
        for key,value in dataDict.items():
            fields.append({
                "type": "mrkdwn",
                "text": f"*{key} :* \n {value}"
                }
            )
        payload['blocks'][0]['fields']=fields

        requests.post(
            self.HOOK_LINK,
            headers={'Content-Type':'application/json'},
            json=payload
        ).text