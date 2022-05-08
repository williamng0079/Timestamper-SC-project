## This is test will be ran on both private local ganache node and ropsten public testnet (more realistic environment) 
# this script will perform timestamping of a sha256 hash multiple times 
#   in order to gather test data to determine the average time delay 
# the difference is taken between immediately before input submission and immediately after block confirmation
# (this test does not take into account limitations such as situations where the ethereum forks)
# (this test also does not take into account of failed transactions, 
#  it assumes that all transactions are successful (i.e., status = 1 on the receipt))
# This hash will be used repeatedly: 4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e
# The results will be plotted with matplotlib to provide a visualisation of the test data.
# Block interval for the private local ganache node has been set to 13s as it is the average time for the main net

# NB:  
# Order transactions within each block will be decided by the winning miner of block generation even if a smart contract is being called simultaneously
# (Source: https://ethereum.stackexchange.com/questions/2856/what-happens-when-a-smart-contract-gets-several-similar-calls-in-the-same-block)
# the cli interactor is designed to wait for the block confirm before any other request can be made
# therefore, the average delay time is expected to be consistent with the time taken for the block generations (ignoring forks)
# the result of this experiment can be used to determine a timeout option for the wait for block receipt feature)

#   the batch timestamp feature was implemented to solve the issue of only one transaction is made per block for the interactor.
#       (i.e., with default timestamp function, that means only one hash can be submitted per block generation)



# Three types of tests will be conducted for the timestamp delay 
# 1.   Test the time delay for the cli code, i.e., 
# single request per block confirmation (the result of average time delay is expected to be consistent to the block interval of the node)
# in the case of the ganache local node, as the block interval is set to 13s to mimic the avg ethereum block interval, the avg time delay of transaction is expected to be extremely close to 13s
# 2.   Test time delay when transaction requests are submitted in a continuous fashion, i.e., input are supplied continuously 
# test 2 can be achieved with the multiprocessing library 
# for test two the expected avg delay is at around 7s over a large number of requests (13/2)
# display average on the plotted graph

#3.    This test case aims to uncover the addtional time delay in seconds per additional element within the list of the of batch timestamp feature.

## overall relatively linear relationship as expected, anomalies and spike in time is detected for unknown reason. 
# (maybe the difference in hash value?) tested: the value of the hash does not contributed to the reason of spikes in time


import time
import multiprocessing as mp
from xml.dom.minidom import Element
from web3 import Web3 
import sys
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import binascii


# logic 4: store the difference into an array 
# logic 5: plot the data within the array: time delay on y axis and the transaction occurrence on x axis
load_dotenv()                                           
node_provider = os.environ['LOCAL_NODE_PROVIDER']        
Timestamper_abi = json.loads(os.environ['CONTRACT_ABI']) 
contract_address = os.environ['SMART_CONTRACT_ADDRESS']
owner_account = os.environ['OWNER_ADDRESS']
web3_connection = Web3(Web3.HTTPProvider(node_provider)) 
web3_connection.eth.default_account = owner_account

def generate_hash():
    random_hash_string = binascii.b2a_hex(os.urandom(32)).decode("utf-8")
    #print(random_hash_string)
    return random_hash_string


def get_time_diff(before, after):
    time_diff = after - before
    in_sec = time_diff.total_seconds()      #(Source: https://geekflare.com/calculate-time-difference-in-python/#:~:text=To%20calculate%20the%20total%20time,birthday%20is%2019017960.127416%20seconds%20away.)

    return in_sec


def delay_test_case_1():
    global delay_list 
    
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)
    time_before = datetime.now()
    input_tx_hash = contract.functions.timestamp("4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e").transact() 
    web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)
    time_after = datetime.now()
    delay_value = (time_after - time_before).total_seconds()
    print(delay_value)
    delay_list.append(delay_value)
    
    return delay_value


#logic: loop transaction, get time before submit and time after wait for receipt
# the time of submission is taken right before the input is being processed by the smart contract
def delay_test_case_2():
    
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)
    time_before = datetime.now()
    input_tx_hash = contract.functions.timestamp("4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e").transact()  
    web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)
    time_after = datetime.now()
    delay_value = (time_after - time_before).total_seconds()
    
    print(delay_value)
    
    with open ("../Timestamper-SC-project/Test_data_generation/Continuous_Delay.txt", "a") as testcase_2:
        testcase_2.write(str(delay_value))
        testcase_2.write("\n")
    return delay_value

## logic: get the avg extra time required with additional element in the batch timestamp funtion

#  for this test, ganache is set to automine as block interval time does not need to be taken into account,
#  as the test purpose is to obtain the addition time required for each additional element in the batch timestamp list
#  hash generation for this will be random instead of a constant hash value for extra realism
def delay_test_case_3(hash_list):
    
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)
    time_before = datetime.now()
    input_tx_hash = contract.functions.batchTimestamp(hash_list).transact()  
    web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)
    time_after = datetime.now()
    delay_value = (time_after - time_before).total_seconds()
    
    return delay_value



if __name__ == "__main__":
    os.system("clear")
    print("select timestamping delay test:")
    print("\n1. Test case 1: Single transaction request per block generation")
    print("\n2. Test case 2: Consecutive transaction request")
    print("\n3. Test case 3: Increase in time per additional element in the batch timestamp list")
    selection = input("\nInput >>>")
    
    
    if selection == "1":
        print("\nINITIATING TEST CASE 1: SINGLE REQUEST PER BLOCK...\n")
        delay_list = []
        for i in range (100):
            delay_test_case_1()
        
        

        print("\nPlease use data_analyser.py to visualise the obtained data and obtain an average value")
        

    elif selection == "2":
        print("INITIALISING TEST CASE 2: CONTINUOUS REQUEST.....")
        print("\nPROGRAM WILL AUTO TERMINATE WHEN COMPLETE, RESULTS WILL BE WRITTEN TO -- Continuous_Delay.txt--")
        open("../Timestamper-SC-project/Test_data_generation/Continuous_Delay.txt", "w").close         
        # this is to ensure data in the file from the previous test instance is erased
            
        print("Use data_analyser.py to obtain the average value and graph of the data ")
        for i in range (300):
            mp.Process(target = delay_test_case_2).start()
            time.sleep(0.3)                   
#within the block interval, the number of transaction requests is limited, by setting the 0.3s interval between each request, 
#it avoids the problem where too many requests are queued at once which results in delay time that is significantly longer than block interval.
    
    elif selection == "3":
        print("INITIATING TEST CASE 3: ADDITIONAL TIME DELAY PER ELEMENT IN BATCH TIMESTAMP LIST.......")
        input_list = []
        delay_list = []
        for i in range(100):
            #new_hash = generate_hash()
            input_list.append("4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e")                           # modify this line to experiment with the same hash value appending to the list each time
            delay_time = delay_test_case_3(input_list)
            print(delay_time)
            delay_list.append(delay_time)
        
        print("\nList of data generated:", delay_list)
        print("\nOUTPUTING TEST DATA TO FILE --Batch_Delay.txt--")
        with open("../Timestamper-SC-project/Test_data_generation/Batch_Delay.txt", "w") as testcase_3:
            for i in delay_list:
                testcase_3.write(str(i))
                testcase_3.write("\n")

        
    else:
        print("Unregistered Input please restart, terminating tests.......")
        sys.exit()
    