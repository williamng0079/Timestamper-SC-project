#This program will allow the user to supply hash values to the deployed smart contract
#This program does not compile nor deploy the solidity contracts, ensure that the contracts are compiled and deployed via truffle.
#By utilising the web3 library, functions within the DEPLOYED contract can be called here
#Majority of the computation (input validation, cli, extracting transaction receipt attributes etc...)will be done here to reduce the computation done by the solidity smart contract to reduce gas usage which lowers cost (gas fee)
#This program will read the .env file in the home directory in order to retrieve required values for the smart contract interaction.
####### Ensure that the .env are updated with the correct contract information before each interaction #######
import re
from socket import SO_DONTROUTE
import sys
import os
import json
from dotenv import load_dotenv
from web3 import Web3                       #(Source: https://web3py.readthedocs.io/en/stable/)
import string
import time
import getpass
from binascii import hexlify                #(Source: https://www.delftstack.com/howto/python/python-convert-byte-to-hex/)
import pyfiglet
from datetime import datetime               #(Source: https://www.programiz.com/python-programming/datetime/current-datetime)
import pprint as pp                         #(Source: https://docs.python.org/3/library/pprint.html#pprint.pprint)


load_dotenv()                                            #loading environment constants stored within the .env file

node_provider = os.environ['LOCAL_NODE_PROVIDER']        
Timestamper_abi = json.loads(os.environ['CONTRACT_ABI']) #and abi is the contract application binary interface used for smart contract interaction, it is encoded in the json format (Source: https://docs.soliditylang.org/en/v0.8.13/abi-spec.html)
contract_address = os.environ['SMART_CONTRACT_ADDRESS']
owner_account = os.environ['OWNER_ADDRESS']

web3_connection = Web3(Web3.HTTPProvider(node_provider)) #connecting to the ethereum node 
web3_connection.eth.default_account = owner_account      #identifing the account address to be used to send transactions
                                                         #note that the default account must be the account that deployed the smart contract due to the access control implement with Ownable


def connection_status():
    #print(web3_connection.isConnected())                 #connection check, if successfully connected to the node, it will return true
    return web3_connection.isConnected()
    
def interact(hash, batch = False):                                     #takes a single user input (hash) as argument to be logged into the solidity event log
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)  #initiating an object for the deployed contract. 
    if (batch == True):
        input_tx_hash = contract.functions.batchTimestamp(hash).transact()              #.transact() will returns the transaction hash.
        tx_receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)    #as name suggests, wait_for_transaction_receipt will ensure that the transaction has been included within a block (Source: https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.wait_for_transaction_receipt)
    else:
        input_tx_hash = contract.functions.timestamp(hash).transact()      #this will perform a transaction in order the modify the state of the deployed smart contract
        tx_receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)                                                               
    
    return tx_receipt


def write_to_file(receipt):
    with open("transaction_logs.txt", "a") as logfile:
        pp.pprint(receipt, logfile, sort_dicts=False)                                 #(Source: https://docs.python.org/3/library/pprint.html#pprint.pprint)
        logfile.write("\n\n\n")
    

## target input: can only be 32 digits or 64 digits (either md5 or sha256) note maybe discard the option for MD5
##        contains only alphanumeric other than other than 0-9, and a-f (alphanumeric) (Source: https://careerkarma.com/blog/python-isalpha-isnumeric-isalnum/)
##        check if 0x prefix exist, fail if it does as hexdigits check will fail, because "x"
def validate(s):
    
    if len(s) < 65 and s.isalnum() == True:                         #(Source: https://careerkarma.com/blog/python-isalpha-isnumeric-isalnum/)
        validation = all(c in string.hexdigits for c in s)          #(Source: https://stackoverflow.com/questions/11592261/check-if-a-string-is-hexadecimal)
    else:
        validation = False
    return validation


def single_input():
    print("\n\n---Please supply a hash (without the '0x' prefix)---\nEnter quit to go back\n\n")
    userInput = input("Enter your value >>")
    if userInput == "quit": 
        print("\nNothing has been submitted to the smart contract\n")  
        userInput = 0
        time.sleep(3)    
    elif validate(userInput) == False:
        print("\nSorry, the input cannot be processed, please enter a correct hash\n")
        print("\nReturning to the main menu...\n")
        userInput = 0     
        time.sleep(3)    
    else: 
        print("\nThe entered value: "+userInput+" will be recorded onto the blockchain!!!\n")
    return userInput

#logic: ask user to supply 1 element each time, store into a string array, ignore any input that fails validation and store the next one.

def batch_input():
    hash_array = []
    print("\n\n---Please supply a hash (without the '0x' prefix)---\nEnter done to finish the submission\nEnter quit to discard submission\n\n")
    while True:
        userInput = input("Enter your value >>")
        if userInput == "quit":
            hash_array = 0
            print("\nuser quits the submission\n")
            time.sleep(3)
            break
        elif userInput == "done":
            if hash_array == []:
                print("\nnothing is entered to the array\n")
                time.sleep(3)
            else:
                print("\nuser submitted the following values:\n")
                print(hash_array)
                print("\n\n")
            break
        elif validate(userInput) == False:
            print("\nSorry, the input cannot be processed, please enter a correct hash\n")
            
        else:
            hash_array.append(userInput)
    return hash_array 


## logic: take the block receipt AttributeDict as argument and filters out the useful information to be displayed or used for tests
## Note that the same information can be check on the nodes (ganache for local, etherscan for Ropsten)
## Useful information to be logged and to be display on the terminal in a more readable format
def reconstruct_receipt(tx_receipt, time, userInput, sender):
    receipt = {}
    receipt["Time_of_Transaction_Confirmed"] = str(time)
    receipt["User_Input"] = userInput
    receipt["Transaction_Hash"] = hexlify(tx_receipt.transactionHash).decode("utf-8")
    receipt["Block_Hash"] = hexlify(tx_receipt.blockHash).decode("utf-8")
    receipt["Block_Number"] = tx_receipt.blockNumber
    receipt["From"] = sender
    receipt["To"] = tx_receipt.to
    receipt["Gas_Used"] = tx_receipt.gasUsed
    receipt["Cumulative_Gas_Used"] = tx_receipt.cumulativeGasUsed
    receipt["Status"] = tx_receipt.status
    
    return receipt
    
def process_single():
    outcome = single_input()    
    if outcome == 0:
        status = 0
    else:    
        transact = interact(outcome)
        time_get = datetime.now()
        receipt_dict = reconstruct_receipt(transact, time_get, outcome, owner_account)
        #print("Full transaction receipt:\n". transact)         #to see unfiltered and complete block transaction receipt, uncomment this line
        print("Transaction receipt:")
        pp.pprint(receipt_dict, sort_dicts=False)
        print("\n\n\n--- IMPORTANT INFORMATION ---")
        print("\nMAKE SURE YOU SAVE THE TRANSACTION HASH TO CHECK THE DETAIL OF THE SUBMITTED HASH IN THE FUTURE")
        print("\n\nTime of transaction confirmed:", time_get)
        print("\nYou have submitted:", outcome)
        print("\nTransaction status:", transact.status)
        print("\nTransaction hash:",hexlify(transact.transactionHash).decode("utf-8"))
        print("\nGas Used:", transact.gasUsed)
        
        getpass.getpass("\n\n\nPress Enter to continue...")
        write_to_file(receipt_dict)
        status = 1
    return status

def process_batch():
    outcome = batch_input()
    if outcome == []:
        status = 0
    elif outcome == 0:
        status = 0
    else:
        transact = interact(outcome, True)
        time_get = datetime.now()
        receipt_dict = reconstruct_receipt(transact, time_get, outcome, owner_account)
        #print("Full transaction receipt:\n". transact)         #to see unfiltered and complete block transaction receipt, uncomment this line
        print("Transaction receipt:")
        pp.pprint(receipt_dict, sort_dicts=False)
        print("\n\n\n--- IMPORTANT INFORMATION ---")
        print("\nMAKE SURE YOU SAVE THE TRANSACTION HASH TO CHECK THE DETAIL OF THE SUBMITTED HASH IN THE FUTURE")
        print("\n\nTime of transaction confirmed:", time_get)
        print("\nYou have submitted:", outcome)
        print("\nTransaction status:", transact.status)
        print("\nTransaction hash:",hexlify(transact.transactionHash).decode("utf-8"))
        print("Gas Used:", transact.gasUsed)
        
        getpass.getpass("\n\n\nPress Enter to continue...")
        write_to_file(receipt_dict)
        status = 1
    return status

def welcome():
    print(pyfiglet.figlet_format("ETHEREUM TIMESTAMPTER", font = "cybermedium"))
    #print(pyfiglet.figlet_format("welcome"))


## make sh scripts to deploy on both ganache and ropsten and update .env automatically.
##        think about adding options to enable network selection
def terminal():
    while(True):
        os.system("clear")
        welcome()
        print("\n\nConnecting to the Ethereum node.......\n\n")
        
        if connection_status() == True:
            print("Successfully connected to...\n")
        else:
            print("Connection cannot be established, check the following:\n")
            print("1. Ensure that the smart contract has been deployed (Ganache and/or Ropsten testnet)")
            print("2. The .env file has the correct smart contract deployment and owner address")
            print("3. If deployed locally, please make sure Ganache is running in the background\n")
            sys.exit()
    
        print("What would you like to do?\n")
        print("1. Press 1 for single timestamp")
        print("2. Press 2 for batch timestamp\n")
        print("Enter exit to terminate program\n")
        while(True):
            userIn = input("Input >>>")
            if userIn == "exit":
                os.system("clear")
                sys.exit()
            elif userIn == "1":
                print("\nEntered single mode")
                process_single()
                
                break
            elif userIn == "2":
                print("\nEntered batch mode")
                process_batch()
                
                break
            else:
                print("\nInvalid input "+userIn+"\n")

             
terminal()
#welcome()