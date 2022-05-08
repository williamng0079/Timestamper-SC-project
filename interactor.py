## This program will allow the user to submit hash values to the deployed smart contract.
## This program does not compile nor deploy the solidity contracts, ensure that the contracts are compiled and deployed via truffle.
## Majority of the computation will be done here(input validation, cli, extracting transaction receipt attributes etc...)
## This is to ensure minimum computation done when calling the smart contract to reduce the usage of gas unit which will eventually lowers cost (gas fee).
## This program will read the .env file in the home directory in order to retrieve required values for the smart contract interaction.
####### Ensure .env is updated with the correct deployment information (smart contract deployed address, owner address) before each interaction #######
import sys
import os
import json
from dotenv import load_dotenv
from web3 import Web3                       
import string
import time
import getpass
from binascii import hexlify                
import pyfiglet                             #(Source: https://pypi.org/project/pyfiglet/0.7/)
from datetime import datetime               
import pprint as pp                         

# Connection check, if successfully connected to the node, it will return true.
def connection_status():
    # print(web3_connection.isConnected())                 
    return web3_connection.isConnected()


def interact(hash, batch = False):                       
    
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)  
    # Allows the deployed contract to be interacted as they were JavaScript objects (Python, n.d.). 
    
    if (batch == True): # If batch flag is called with true, batchTimestamp funtion within the smart contract will be called
        
        input_tx_hash = contract.functions.batchTimestamp(hash).transact()              
        #.transact() will returns the transaction hash.

        tx_receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)    
        # As name suggests, wait_for_transaction_receipt will ensure that the transaction has been included within a block (Python, n.d.)
    
    else:   # This calls the single timestamp function.
        input_tx_hash = contract.functions.timestamp(hash).transact()      
        tx_receipt = web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)                                                               
    
    return tx_receipt
    # Return the detailed attribute dict containing transaction information.



def write_to_file(receipt):
    with open("transaction_logs.txt", "a") as logfile:
        pp.pprint(receipt, logfile, sort_dicts=False)                                
        logfile.write("\n\n\n")
        # Use the data pretty printer to presesnt the logged info in a more readable format (Python, n.d.)


# This Funtion will perform string validation before user inputs are parsed to the smart contract
def validate(s):
    
    if len(s) < 65 and s.isalnum() == True:                         
        # This if statement will check if the string value entered is less than 65 digits long 
        # It also makes sure that the input only contains alphanumeric values.

        validation = all(c in string.hexdigits for c in s)          
        # This line will return true if the string arg supplied only contains hex digits (0-9) and (a-f), otherwise, it returns false

    else:
        validation = False

    return validation
    # Returns true if all the checks above are passed.

# This function provides the menu interface for when the user enters single submission mode, it will also execute the string validation function here.
def single_input():
    print("\n\n---Please supply a hash (without the '0x' prefix)---\nEnter quit to go back\n\n")
    # It prompts the user to remove the hex prefix (0x) as x will fail the string validation check

    userInput = input("Enter your value >>")
    if userInput == "quit": 
        print("\nNothing has been submitted to the smart contract\n")  
        userInput = 0
        time.sleep(2)    
    
    elif validate(userInput) == False:
        print("\nSorry, the input cannot be processed, please enter a correct hash\n")
        print("\nReturning to the main menu...\n")
        userInput = 0     
        time.sleep(2)    
    
    else: 
        print("\nThe entered value: "+userInput+" will be recorded onto the blockchain!!!\n")
    
    return userInput
    # It will return the user input if such input has passed the string validation and is not a quit command, otherwise it will return 0


# This function provides the menu interface to allow the user to submit a list of values, 
# it opens with a while loop to allow appending each input entered by the user to a list continuosly.
# there are three checks per input: 
# 1. user entered quit command to traverse back to the main menu 
# 2. user input either pass or fail the string validation check
# 3. user entered done but did not submit anything, if the list isnt empty, 
#      it will display the content and return the list to be processed by the smart contract.
def batch_input():
    hash_list = []
    print("\n\n---Please supply a hash (without the '0x' prefix)---\nEnter done to finish the submission\nEnter quit to discard submission\n\n")
    while True:
        userInput = input("Enter your value >>")
        if userInput == "quit":
            hash_list = 0
            print("\nuser quits the submission\n")
            time.sleep(2)
            break
        
        elif userInput == "done":
            if hash_list == []:
                print("\nnothing is entered to the array\n")
                time.sleep(2)
            else:
                print("\nuser submitted the following values:\n")
                print(hash_list)
                print("\n\n")
            break
        
        elif validate(userInput) == False:
            print("\nSorry, the input cannot be processed, please enter a correct hash\n")
            
        else:
            hash_list.append(userInput)
    
    return hash_list 

# The below funtion will return the Keccak 256 hash a string value parsed, 
# if the list flag is called with true, thi function will iterate through the list and convert every single string inside, 
# then, it will outputs a list of keccak 256 hashes in the same order.
def Convert_to_keccak(value, list=False):
    
    if list == True:
        keccak_list = []
        for i in value:
            keccak_b = Web3.keccak(text=i)  
            # Web3.keccak returns the hash of the value parsed (Python, n.d.)
            
            readable = hexlify(keccak_b).decode("utf-8")
            keccak_list.append(readable)
        
        return keccak_list
    
    else:
        keccak_b = Web3.keccak(text=value)
        readable = hexlify(keccak_b).decode("utf-8")
        
        return readable


# This function will take the transaction receipt returned by the interact function and retrieve crucial attributes from it,
# it also takes other useful information such as time of receipt and user input of the transaction.
# then, it will store them in a python dictionary for both terminal display and local log file (to be pretty printed for a more readable format).
def reconstruct_receipt(tx_receipt, time, userInput, sender):
    receipt = {}
    receipt["Time_of_Transaction_Confirmed"] = str(time)
    receipt["User_Input"] = userInput
    receipt["Transaction_Hash"] = hexlify(tx_receipt.transactionHash).decode("utf-8")
    # The hexlify function will convert the byte representation to hex and .decode will remove the b' prefix so it is displayed in a string format (Python, n.d.)
    
    receipt["Block_Hash"] = hexlify(tx_receipt.blockHash).decode("utf-8")
    receipt["Block_Number"] = tx_receipt.blockNumber
    receipt["From"] = sender
    receipt["To"] = tx_receipt.to
    receipt["Gas_Used"] = tx_receipt.gasUsed
    receipt["Cumulative_Gas_Used"] = tx_receipt.cumulativeGasUsed
    receipt["Status"] = tx_receipt.status
    return receipt


# This function will take the reconstructed transaction receipt and perform pretty print for user friendly display of the transacition detail.
def transaction_message(_receipt, _time, _input, _transact, _kVal):
    print("Transaction receipt:")
    pp.pprint(_receipt, sort_dicts=False)
    # The false sort_dict flag ensures that the order of the reconstructed receipt isn't sorted in alphabetical order.

    print("\n\n\n---!!! IMPORTANT INFORMATION !!!---")
    print("\nMAKE SURE YOU SAVE THE TRANSACTION HASH AND THE KECCAK256 VALUES OF YOUR SUBMISSIONS FOR FUTURE REFERENCE OF THE TIMESTAMPS")
    print("\nWITHOUT THE TRANSACTION HASH, YOU WILL NOT BE ABLE TO FIND THE TIMESTAMP IN THE FUTURE")
    print("\nTHE KECCAK256 VALUES ARE YOUR SUBMISSIONS HASHED AGAIN BY SOLIDITY KECCAK AND IT WILL BE SHOWN ON THE LOG PAGE OF YOUR NODE PROVIDER")
    print("\n\nTime of transaction confirmed:", _time)
    print("\nYou have submitted:\n")
    pp.pprint(_input)
    print("\nKeccak256 values of your submissions (in order):\n")
    pp.pprint(_kVal)
    # If the _kVal is a list, it will print it a value per row.

    print("\n\nTransaction status:", _transact.status)
    print("\nTransaction hash:",hexlify(_transact.transactionHash).decode("utf-8"))
    print("\nGas Used:", _transact.gasUsed)

# The function below will process the smart contract transaction and call a series of predefined functions above.
def process_single():
    outcome = single_input()    
    if outcome == 0:
        status = 0
    else:    
        transact = interact(outcome)
        time_get = datetime.now()
        receipt_dict = reconstruct_receipt(transact, time_get, outcome, owner_account)
        #print("Full transaction receipt:\n". transact)         #to see unfiltered and complete block transaction receipt, uncomment this line
        keccak_value = Convert_to_keccak(outcome)
        transaction_message(receipt_dict, time_get, outcome, transact, keccak_value)
        getpass.getpass("\n\n\nPress Enter to continue...")
        write_to_file(receipt_dict)
        # writes useful informaiton of the transaction to a local log file for future reference
        status = 1
    return status

# This function will call a series of functions to process the list of hashes.
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
        #print("Full transaction receipt:\n". transact)         #to see raw unfiltered block transaction receipt, uncomment this line.
        keccak_value = Convert_to_keccak(outcome, True)
        transaction_message(receipt_dict, time_get, outcome, transact, keccak_value)
        getpass.getpass("\n\n\nPress Enter to continue...")
        write_to_file(receipt_dict)
        status = 1
    return status

# Welcome screen of the CLI (Command Line Interface)
def welcome():
    print(pyfiglet.figlet_format("ETHEREUM TIMESTAMPTER", font = "cybermedium"))
    # pyfiglet is used to convert text into ascii blocks that looks aesthetcally pleasing (Waller, 2019).
    


# This function is the main function to be called to initial the CLI, it calls functions defined above depending on the user input.
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
                
                
# Avoid the following being executed in another code what imports functions from this code
if __name__ == "__main__":                  
    
    load_dotenv()                                           
    # Loading environment constants stored within the .env file.

    node_provider = os.environ['LOCAL_NODE_PROVIDER']        
    Timestamper_abi = json.loads(os.environ['CONTRACT_ABI']) 
    # abi is the contract application binary interface used for smart contract interaction, 
    # it is encoded in the json format (Solidity, n.d.) (Source: https://docs.soliditylang.org/en/v0.8.13/abi-spec.html)
    
    contract_address = os.environ['SMART_CONTRACT_ADDRESS']
    owner_account = os.environ['OWNER_ADDRESS']
    web3_connection = Web3(Web3.HTTPProvider(node_provider)) 
    # Default connection: connecting to the local private Ethereum node provided by Ganache
    
    web3_connection.eth.default_account = owner_account      
    # Identifing the account address to be used to send transactions (it has to be the address that deployed the contract)
                                                                                        
    terminal()
    