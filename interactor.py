#This program will act as the gateway for the user to supply hash values to the deployed smart contract
#This program does not compile nor deploy the solidity contracts, ensure that the contracts are compiled and deployed via truffle.
#By utilising the web3 library, functions within the DEPLOYED contract can be called here
#Majority of the computation will be done here to reduce the computation done by the solidity smart contract to reduce gas usage which lowers cost (gas fee)
#This program will read the .env file in the home directory in order to retrieve required values for the smart contract interaction.
####### Ensure that the .env are updated with the correct contract information before each interaction #######
import sys
import os
import json
from dotenv import load_dotenv
from web3 import Web3
import string

load_dotenv()                                            #loading environment constants stored within the .env file

node_provider = os.environ['LOCAL_NODE_PROVIDER']        
Timestamper_abi = json.loads(os.environ['CONTRACT_ABI']) #and abi is the contract application binary interface used for smart contract interaction, it is encoded in the json format (Source: https://docs.soliditylang.org/en/v0.8.13/abi-spec.html)
contract_address = os.environ['SMART_CONTRACT_ADDRESS']
owner_account = os.environ['OWNER_ADDRESS']

web3_connection = Web3(Web3.HTTPProvider(node_provider)) #connecting to the ethereum node 
web3_connection.eth.default_account = owner_account      #identifing the account address to be used to send transactions
                                                         #note that the default account must be the account that deployed the smart contract due to the access control implement with Ownable


def connection_status():
    print(web3_connection.isConnected())                 #connection check, if successfully connected to the node, it will return true

    
def interact(hash, batch = False):                                     #takes a single user input (hash) as argument to be logged into the solidity event log
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)  #initiating an object for the deployed contract. 
    if (batch == True):
        input_tx_hash = contract.functions.batchTimestamp(hash).transact()              #.transact() will returns the transaction hash.
        tx_receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)    #as name suggests, wait_for_transaction_receipt will ensure that the transaction has been included within a block (Source: https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.wait_for_transaction_receipt)
    else:
        input_tx_hash = contract.functions.timestamp(hash).transact()      #this will perform a transaction in order the modify the state of the deployed smart contract
        tx_receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)                                                               
    
    return tx_receipt


## target input: can only be 32 digits or 64 digits (either md5 or sha256) note maybe discard the option for MD5
##        contains only alphanumeric other than other than 0-9, and a-f (alphanumeric)
def validate(s):
    
    if len(s) < 65 and s.isalnum() == True:
        validation = all(c in string.hexdigits for c in s)
    else:
        validation = False
    return validation


def single_input():
    userInput = input("Please supply a hash, or enter quit to terminate:")
    if userInput == "quit": 
        userInput = 0
        print("Nothing has been submitted to the smart contract")        
    elif validate(userInput) == False:
        print("Sorry, the input cannot be processed, please enter a correct hash")
        userInput = 0         
    else: 
        print("The entered value: "+userInput+" will be recorded onto the blockchain!!!")
    
    return userInput

#logic: ask user to supply 1 element each time, store into a string array, ignore any input that fails validation and store the next one.

def batch_input():
    hash_array = []
    while True:
        userInput = input("Please supply a hash, enter done to finish the submission, enter quit to discard submission:")
        if userInput == "quit":
            hash_array = 0
            print("user quits the submission")
            break
        elif userInput == "done":
            if hash_array == []:
                print("yessir, nothing is entered to the array")
            else:
                print("user submitted the following:")
                print(hash_array)
            break
        elif validate(userInput) == False:
            print("Sorry, the input cannot be processed, please restart and enter a correct hash")
        else:
            hash_array.append(userInput)
    return hash_array 


def process_single():
    outcome = single_input()    
    if outcome == 0:
        sys.exit()
    else:    
        transact = interact(outcome)
        print(transact)


def process_batch():
    outcome = batch_input()
    if outcome == []:
        sys.exit()
    elif outcome == 0:
        sys.exit()
    else:
        transact = interact(outcome, True)
        print(transact)

#process_single()
#process_batch()