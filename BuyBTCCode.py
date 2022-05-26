import cbpro
import os
from dotenv import load_dotenv
import azure.functions as func

#def main():
def main(mytimer: func.TimerRequest) -> None:
    #set variables
    pair = "BTC-GBP"
    fund = "2.00"
    #size = "0.00000"


    #load environment variables
    load_dotenv()
    key = os.getenv('KEY')
    secret = os.getenv('SECRET')
    passphrase = os.getenv('PASSPHRASE')

    #create authorised client
    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)

    #place buy order
    auth_client.place_market_order(product_id=pair, side='buy', funds=fund)

