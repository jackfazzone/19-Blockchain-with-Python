import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
load_dotenv()
from web3 import Web3

print("RAN")

mnemonic = os.getenv('MNEMONIC', 'pill wink release wink vivid shy flame estate giraffe initial gadget eagle copper lucky absent')
print(mnemonic)
command = 'php -g --mnemonic="pill wink release wink vivid shy flame estate giraffe initial gadget eagle copper lucky absent" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)
