## This test script will test specifically the batchtimestamp feature of the smart contract,
## the gas usage increase per 1 additional element within the list batch timestamp feature will be recorded.
## The rate of increase in gas per additional element in a list is expected to be constant (the plotted graph is expected to be diagnal straight line).
## This test is conducted with ganache set to automine meaning that there isn't a block interval time as time is not a factor in this test.
from web3 import Web3 
import os
import json
from dotenv import load_dotenv
import binascii
import sys
sys.path.append('../Timestamper-SC-project/')

# Loading the required variables for smart contract interaction from the environment file
load_dotenv()                                           
node_provider = os.environ['LOCAL_NODE_PROVIDER']        
Timestamper_abi = json.loads(os.environ['CONTRACT_ABI']) 
contract_address = os.environ['SMART_CONTRACT_ADDRESS']
owner_account = os.environ['OWNER_ADDRESS']
web3_connection = Web3(Web3.HTTPProvider(node_provider)) 
web3_connection.eth.default_account = owner_account


# This function will generate a random hex string that is 64 digits long, this is used to simulate sha256 hash
def generate_hash():
    random_hash_string = binascii.b2a_hex(os.urandom(32)).decode("utf-8")
    #print(random_hash_string)
    return random_hash_string

# Create the smart contract instance and performs transaction to call the batchTimestamp function.
def transact(_input):
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)
    input_tx_hash = contract.functions.batchTimestamp(_input).transact() 
    receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)
    gasUsage = receipt.gasUsed
    # Retrieve the gas usage of the smart contract call from the block confirmation receipt

    return gasUsage
    

if __name__ == "__main__":
    
    input_list = []
    gas_list = []

    # For each iteration of the loop, a new random 64 digits hash string will be generated and appended to the list.
    for i in range(100):    # The range can be modified to test different numbers of element in the batch timestamp list
        new_hash = generate_hash()
        input_list.append(new_hash)
        eth_gas = transact(input_list)
        print(eth_gas)
        gas_list.append(eth_gas)
        # the retrieved gas usage is then appended to the gas usage list for later graph plotting purpose

    # Writes each element of the gas usage list in to a txt data file called Gas_Usage which will then be processed by the data analyser script.
    with open("../Timestamper-SC-project/Test_data_generation/Gas_Usage.txt","w") as gasfile:
        for i in gas_list:
            gasfile.write(str(i))
            gasfile.write("\n")

    print(gas_list)

