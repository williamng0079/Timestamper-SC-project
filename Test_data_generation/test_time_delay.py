## This script will be testing three scenarios relating to the delay in the timestamping user inputs
## The time delay tested in this script does not take into account the situation where the blockchain fork occurs as such factor is unpredicatble.
## Additionally, this test does not take into account failed transactions caused by various reasons (e.g.,out of gas)
## The timestamps are taken at two points of the execution for the difference calculation:
##      Before: the timestamp right before the input submission and the function call.
##      After: the timestamp right after block confirmation receipt is received.
import time
import multiprocessing as mp
from web3 import Web3 
import sys
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import binascii
sys.path.append('./Timestamper-SC-project/')

# Loads the environment constants and store required values into variables.
load_dotenv()                                           
node_provider = os.environ['LOCAL_NODE_PROVIDER']        
Timestamper_abi = json.loads(os.environ['CONTRACT_ABI']) 
contract_address = os.environ['SMART_CONTRACT_ADDRESS']
owner_account = os.environ['OWNER_ADDRESS']
web3_connection = Web3(Web3.HTTPProvider(node_provider)) 
web3_connection.eth.default_account = owner_account

# This generate a random hex string with the length of 64 upon each call.
def generate_hash():
    random_hash_string = binascii.b2a_hex(os.urandom(32)).decode("utf-8")
    #print(random_hash_string)
    return random_hash_string

# This will perform simple subtraction of two timestamps and obtain the difference in seconds
def get_time_diff(before, after):
    time_diff = after - before
    in_sec = time_diff.total_seconds()      
    return in_sec


## 1. Test the delay in seconds for single transaction request per block confirmation.
##    The hash input value to be used for this test is: 4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e
##    This test needs be conducted with the block interval set to 13 seconds, as 13s is the average interval for the main net.
##    timestamp function is called for this test.
##    The test result is expecetd to be consistent with the block generation (interval) time, in this case, ~13s.
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
    # Upon each function call, the input argument will be submitted and timestamp function will be called,
    # The delay time is calculated and appended to the global delay_list for later data visualisation.

    return delay_value


## 2. Test the delay in seconds for a continuous stream of transaction requests with a 0.3 seconds interval to avoid over queuing requests.
##    The hash input value to be used for this test is: 4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e
##    This test needs be conducted with the block interval set to 13 seconds, as 13s is the average interval for the main net.
##    timestamp function is called for this test.
##    The test result is expected to show a varying delay time from 0 to 13 seconds with the average at around 7s.
##    The average value retrieved by the test will most likely be applicable to the normal usecase as request can be made at any point within the block interval.
def delay_test_case_2():
    
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)
    time_before = datetime.now()
    input_tx_hash = contract.functions.timestamp("4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e").transact()  
    web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)
    time_after = datetime.now()
    delay_value = (time_after - time_before).total_seconds()
    
    print(delay_value)

    # This test will be perform with multiprocessing library, hence each time the time delay will be appended to an external data file
    with open ("../Timestamper-SC-project/Test_data_generation/Continuous_Delay.txt", "a") as testcase_2:
        testcase_2.write(str(delay_value))
        testcase_2.write("\n")
    return delay_value


## 3. Test the time delay of processing batch timestamping feature based on the number of 64 digits hex values in the list
##    The hash values will be randomly generated and appended (+1) to the submission list on each iteration.
##    This test only considers the relative extra time required per extra element in the list, hence block interval time can be set to 0 (automining mode in Ganache)
##    batchTimestamp function is called for this test.
##    Overall relatively linear growth is expected for this test. 
def delay_test_case_3(hash_list):
    
    contract = web3_connection.eth.contract(address=contract_address, abi=Timestamper_abi)
    time_before = datetime.now()
    input_tx_hash = contract.functions.batchTimestamp(hash_list).transact()  
    web3_connection.eth.wait_for_transaction_receipt(input_tx_hash)
    time_after = datetime.now()
    delay_value = (time_after - time_before).total_seconds()
    
    return delay_value



if __name__ == "__main__":
    ## Simple CLI for user to select what test they would like to do.
    os.system("clear")
    print("Select timestamping delay test:")
    print("\n For test case 1 & 2, please ensure the block interval of the node provider is set to 13s")
    print("\n For test case 3, set the block interval back to 0 (automining mode in Ganache")
    print("\n1. Test case 1: Single transaction request per block generation")
    print("\n2. Test case 2: Consecutive transaction request")
    print("\n3. Test case 3: Increase in time per additional element in the batch timestamp list")
    selection = input("\nInput >>>")
    
    
    if selection == "1":
        print("\nINITIATING TEST CASE 1: SINGLE REQUEST PER BLOCK...\n")
        delay_list = []
        
        for i in range (100):                       # Modify the number in range to change the test parameter
        
            delay_test_case_1()
        with open("../Timestamper-SC-project/Test_data_generation/Single_Delay.txt", "w") as testcase_1:
            for i in delay_list:
                testcase_1.write(str(i))
                testcase_1.write("\n")


        print("\nPlease use data_analyser.py to visualise the obtained data and obtain an average value")
        

    elif selection == "2":
        print("INITIALISING TEST CASE 2: CONTINUOUS REQUEST.....")
        print("\nPROGRAM WILL AUTO TERMINATE WHEN COMPLETE, RESULTS WILL BE WRITTEN TO -- Continuous_Delay.txt--")
        open("../Timestamper-SC-project/Test_data_generation/Continuous_Delay.txt", "w").close         
        # this is to ensure data in the file from the previous test instance is erased
            
        print("Use data_analyser.py to obtain the average value and graph of the data ")
        
        for i in range (300):                       # Modify the number in range to change the test parameter

            mp.Process(target = delay_test_case_2).start()
            # The loop will generate process instances continuously and have them executing in parallel untill the number of processes is equal to the range set above.
            # Too many request process running in parallel will freeze the VM, 300 is tested to be able to produce desirable test result while not being too small.

            time.sleep(0.3)                   
            # Within the block interval, the number of transaction requests is limited, by setting the 0.3s interval between each request, 
            # It avoids the problem where too many requests are queued at once which results in delay time that is significantly longer than block interval.
    

    elif selection == "3":
        print("INITIATING TEST CASE 3: ADDITIONAL TIME DELAY PER ELEMENT IN BATCH TIMESTAMP LIST.......")
        input_list = []
        delay_list = []
        
        for i in range(100):                        # Modify the number in range to change the test parameter
        
            new_hash = generate_hash()
            input_list.append(new_hash)
            #input_list.append("4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e")   # Uncomment this line to test constant hash value in the list
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
    