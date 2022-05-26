import azure.functions as func
import cbpro
import os
from dotenv import load_dotenv
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    #load environment variables
    load_dotenv()
    key = os.getenv('KEY')
    secret = os.getenv('SECRET')
    passphrase = os.getenv('PASSPHRASE')

    #create authorised client
    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)    
    
    #get BTC balance
    balance = 0
    for x in auth_client.get_accounts():
        if x['currency'] == "BTC":
            balance = x['balance']

    #withdraw BTC
    auth_client.crypto_withdraw(balance,"BTC", os.getenv('WITHDRAW'))
