import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
load_dotenv()
from web3 import Web3
import bit

print("RAN")

mnemonic = os.getenv('MNEMONIC')

def derive_wallets(coin):
    command = f'php -g --mnemonic={mnemonic} --cols=path,address,privkey,pubkey --coin={coin} --numderive=3 --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

coins = {'eth':derive_wallets(ETH), 'btc-test':derive_wallets(BTCTEST)}

def priv_key_to_account(coin,privkey)
    if coin == ETH:
        result = Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        result = PrivateKeyTestnet(priv_key)
    else:
        result = "Coin type not ETH or BTC-TEST"
    return result

def create_tx(coin,account,to,amount)
    if coin == ETH:
        gasEstimate = conn.eth.estimateGas({
        "from": account.address,
        "to": to,
        "value": amount
    })
        result = {
        "to": to,
        "from": account.address,
        "value": amount,
        "gasPrice": conn.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": conn.eth.getTransactionCount(account.address)
    }
    elif coin == BTCTEST:
        result = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    else:
        result = "Coin type not ETH or BTC-TEST"
    return result

def send_tx(coin,account,to,amount)
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin== ETH:
        send = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        result = send.hex()

    elif coin == BTCTEST:
        result = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    else:
        result = "Coin type not ETH or BTC-TEST"
    return result

#print(keys)
