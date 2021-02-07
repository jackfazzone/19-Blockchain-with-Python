import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
load_dotenv()
from web3 import Web3
from eth_account import Account
from bit import wif_to_key
from bit import PrivateKeyTestnet
#Citation: https://ofek.dev/bit/guide/advanced.html
from bit.network import NetworkAPI

mnemonic = os.getenv('MNEMONIC')
conn = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print(mnemonic)
def derive_wallets(coin):
    command = f"php derive -g --mnemonic --cols=path,address,privkey,pubkey --coin={coin} --numderive=3 --format=json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    result = json.loads(output)
    return result

coins = {'eth':derive_wallets(ETH), 'btc-test':derive_wallets(BTCTEST)}

def priv_key_to_account(coin,index):
    priv_key = coins[f'{coin}'][index]['privkey']
    if coin == ETH:
        result = Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        result = PrivateKeyTestnet(priv_key)
    else:
        result = "Coin type not ETH or BTC-TEST"
    return result
    

print(priv_key_to_account(ETH,0))
print(priv_key_to_account(BTCTEST,0))

def create_tx(coin,account,to,amount):
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
        "nonce": conn.eth.getTransactionCount(account.address),
        "chainID": conn.net.chainId
    }
    elif coin == BTCTEST:
        result = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTCTEST)])
    else:
        result = "Coin type not ETH or BTC-TEST"
    return result

def send_tx(coin,account,to,amount):
    tx = create_tx(coin, account, to, amount)
    signed = account.sign_transaction(tx)
    if coin== ETH:
        send = conn.eth.sendRawTransaction(signed.rawTransaction)
        result = send.hex()
    elif coin == BTCTEST:
        result = NetworkAPI.broadcast_tx_testnet(signed)
    else:
        result = "Coin type not ETH or BTC-TEST"
    return result

