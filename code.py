from util import mail
from dotenv import load_dotenv
load_dotenv()


mail=SendInBlueMailer()
mail.send_message("Hor sunao kesay ho bhai ?")