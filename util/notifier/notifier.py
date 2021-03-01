from util.mail import SendInBlueMailer
from util.s3 import DigitalOceanSpaces
from .Slack import SlackHook
class Notifier:
  def __init__(self):
    self.mail=mail=SendInBlueMailer()
    self.HTML_CONTENT=open('static/html/email-template.html','r').read()
    self.storage=DigitalOceanSpaces()
    self.slack_hook=SlackHook()

  def send(self,record):
    # Get a link to attach with email
    report_link_for_email=self.storage.get_file_link(record['report_file_name'])

    # 259200-seconds are 3 days
    download_link=self.storage.get_file_link(record['report_file_name'], expireSeconds=259200)

    # Prepare and send Email Notification
    html_content=self.prepare_mail(record)
    self.mail.send_html_message(html_content,report_link_for_email)
    
    # Prepare and Send Slack notification
    payload=self.prepare_slack_message(record,download_link)
    self.slack_hook.send_custom(payload)

  def prepare_mail(self,record):
    html=self.HTML_CONTENT
    html=html\
      .replace("{{crash_id}}",    record["Crash Number"])\
      .replace("{{crash_date}}",  record["Crash Date"].strftime('%m/%d/%Y'))\
      .replace("{{doc_no}}",      record["Document Number"])\
      .replace("{{date_added}}",  record["Add Date"].strftime('%m/%d/%Y'))\
      .replace("{{location}}",    record["Location"])\
      .replace("{{agency}}",      record["Agency"])\
      .replace("{{jurisdiction}}",record["Jurisdiction"])\
      .replace("{{severity}}",    record["Crash Severity"])\
      .replace("{{county}}",      record["County"])
    return html

  def prepare_slack_message(self,record,download_link):
    payload={
      "blocks": [{
        "type": "section",
        "fields": 
          [
            {"type": "mrkdwn","text": "*Crash #*"         +"\n"+ record['Crash Number']},
            {"type": "mrkdwn","text": "*Document #*"      +"\n"+ record['Document Number']},
            {"type": "mrkdwn","text": "*Location:*"       +"\n"+ record['Location']},
            {"type": "mrkdwn","text": "*Crash Date:*"     +"\n"+ record['Crash Date'].strftime('%m/%d/%Y')},
            {"type": "mrkdwn","text": "*Crash Added:*"    +"\n"+ record["Add Date"].strftime('%m/%d/%Y')},
            {"type": "mrkdwn","text": "*Agency:*"         +"\n"+ record['Agency']},
            {"type": "mrkdwn","text": "*Jurisdiction:*"   +"\n"+ record['Jurisdiction']},
            {"type": "mrkdwn","text": "*Crash Severity:*" +"\n"+ record['Crash Severity']},
            {"type": "mrkdwn","text": "*County:*"         +"\n"+ record['County']},
          ]
        },{
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "_This link will expire in 3 Days._"
          },
          "accessory": {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Download Report PDF",
              "emoji": True
            },
            "url": download_link,
          }
      }]
    }
    for rec in record["PdfReportList"]:
      owner=rec["Owner"]
      payload["blocks"][0]["fields"][0].extend([
        {"type": "mrkdwn","text": "*Name:*"         +"\n"+ owner['Name']["first"] +" "+owner['Name']["mid"]+" "+owner['Name']["last"]},
        {"type": "mrkdwn","text": "*Address:*"         +"\n"+ owner['Address']["city"]+", "+owner['Address']["state"]+" "+owner['Address']["zip"]},
      ])
    
    return payload