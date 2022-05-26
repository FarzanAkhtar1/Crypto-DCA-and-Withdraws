from datetime import timedelta
import cbpro
import os
from dotenv import load_dotenv
import itertools
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dateutil import parser
import datetime


import azure.functions as func

#def main():
def main(mytimer: func.TimerRequest) -> None:
    #set variables
    pair = "BTC-GBP"
    currency = "BTC"

    #load environment variables
    load_dotenv()
    key = os.getenv('KEY')
    secret = os.getenv('SECRET')
    passphrase = os.getenv('PASSPHRASE')

    #create authorised client
    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)

    #get details of the buy
    recent_buy_size = 0
    volume = 0
    recent_fills = itertools.islice(auth_client.get_fills(product_id=pair), 1)

    for x in recent_fills:
        volume = str("{:.2f}".format(float(x['price'])*float(x['size'])))
        recent_buy_size = x['size']
        recent_buy_size = x['size']
        yourdate = parser.parse(x['created_at'])
        yourdate = yourdate.replace(tzinfo=None)
        #print(yourdate)

        #print(datetime.datetime.utcnow())
        if datetime.datetime.utcnow() -timedelta(hours=1) <= yourdate:
            yourdate = yourdate.strftime("This was carried out on %d %B %Y at %H:%M")
        else:
            exit()

    #email formation
    message_subject = pair + " purchased"
    message_string = "Purchased "+recent_buy_size+" "+currency+" for £"+volume+"<br>"+yourdate+"<br><br>Thanks,<br>Farzan<br><p style='font-size:10px'>This is an automated message, if you did not expect this please reply to the email.</p>"

    message = Mail(
        from_email=os.getenv('FROM'),
        to_emails=os.getenv('TO'),
        subject=message_subject,
        html_content=message_string)

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)  