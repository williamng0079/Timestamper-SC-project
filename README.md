# 1921139 Dissertation

This readme file will first demonstrate the setup procedures for preparing the environment. 
Then, a list of program executions and descriptions will be provided to demonstrate the development result of this project. 
The below instructions and the setup.sh script have been tested on a fresh Ubuntu 20.04 LTS environment, 
please ensure that they are performed IN ORDER to avoid any potential errors.

mnemonic for Ganache: dad machine patrol lemon atom element menu often dream inch kitten noise

1.  Ganache Download
    Ganache is a local private Ethereum blockchain node provider with an user friendly graphical interface and a built in block explorer (Truffle, n.d.).
    
    Use the link provided below to go to the download page.
    - https://trufflesuite.com/ganache/

    Next, right click the downloaded package, select properties, and within the Permissions section, tick the box that allows executing the file as a program.

    Double click the downloaded package to run the Ganache GUI, and then leave it running in the background.

2.  Run setup.sh to download the required non standard modules for this project

    In termial, within the project root directory, execute the following:
    
    Make the script executable:
    - chmox +x setup.sh             

    Run setup script (make sure that Ganache GUI is running in the background, if not, the download will halt at one point):
    (For detail of the modules, please see within setup.sh, it may take a while to complete)
    - ./setup.sh

3.  Connect the smart contracts to Ganache

    With the modules downloaded from the previous step, return to the Ganache GUI and do the following:
    - Select NEW WORKSPACE (ETHEREUM) 
    - Underneath WORKSPACE, select ADD PROJECT and supply the truffle_config.js file that is present within the project root directory
    - Then, go to the ACCOUNTS & KEYS section and paste the following into the mnemonic field (12 words used to generate consistent key pairs)
            
        mnemonic: dad machine patrol lemon atom element menu often dream inch kitten noise
    
    - Next, click SAVE WORKSPACE at top right to initiate Ganache.


4. Deploy the smart contracts to the local private ethereum blockchain

    Now return to the terminal, within the project directory, execute the following:

    This will perform the contract deployment (it may take a while for the first time)
    - truffle migrate --network development


5. Interact with the deployed Timestamper smart contract 

    With the smart contract deployed, timestamping interaction can be performed with a CLI provided by local_interacter.py
    
    In terminal, within project directory, execute local_interactor.py to perform hash timestamping
    - python3 local_interactor.py

    After the execution, a welcome screen of a CLI will be shown in the terminal, and the following features are provided:

    Mode 1: timestamping a single input of hash values

    Mode 2: timestamping multiple hash input values

    This hash value may be used to test the features described above:

        4f62f6b61e16daa0005c45211abb11a3fd0b8e70cc7f4a1ed1f91cc22a95f78e
    
    (This is the sha256 value of the file hashfile.txt that is present within the project root directory)

    After hash submission, the terminal will return a series of messages and transaction information including statics (i.e., confirmed time, time taken)
    useful information will be written into a log file called local_transaction_logs.txt for future reference.

    Note down the keccak256 value of your submission as this is the evidence of your hash submission shown in the block explorer's log page.

    Next, to confirm that your submission has been timestamped with a block time, go back to the Gananche GUI,
    go to the TRANSACTIONS section, you will be able to see the transaction just made at lot of the list (or alternatively, you can use the transaction hash returned in the transaciton information to search for such transaction, this will be the real world usecase when submissions are submitted to public chains)

    within the transaction page, within the events section, you will be able to see the block time of the block that includes this transaciton and the keccak256 hash mentioned previously in section RETURN VALUES.

    If batch timestamp method was selected, each submission's keccak256 hash value can be found under the events section.


6.  Interact with the same timestamper contract that is deployed to the public Ropsten Ethereum testnet

    The Timestamper smart contract is also deployed to the Ropsten public proof of work network through the Infura node provider with a ropsten test wallet address that contains roughy 2.1 Ropsten test ethers.
    This public deployment is just to test out the contract in a real world use case and it is not the main focus of this disseration.

    For detail of the deployment, see ropsten_deploy_log.txt and truffle-config.js for the wallet mnemonic and Infura project ID 

    To perform timestamping of hash to this public blockchain, do the following:

    In terminal, within the project root directory, initiate connection to the Ropsten net with:
    - truffle console --network ropsten    

    Next, instantiate the contract with the command:
    - const contract = await Timestamper.deployed();

    Then, call the contract with:
        
    single timestamping mode
        - await contract.timestamp("\\enter-the-hash-value-here//")

    batch timestamping function:
        - await contract.batchTimestamp(["\\Enter-hash-here//","\\and-here//","\\and-here//","\\and-more-can-be-added-as-it-is-a-list//","...."])
    
    Wait for the block confirmation receipt, the time delay may vary unlike the main net as Ropsten block inteval is unpredictable due to the fact that there isn't any monetary incentive for the miners to mine new blocks.

    Once the transaction is confirmed, copy the transaction hash and paste it into the public block explorer to search for the record of such transaction:
        https://ropsten.etherscan.io/
    
    The block time can be checked in the timestamp field and teh keccak256 hash of the submission can be checked in the Logs section of the transaction page.


7. Test scripts
    There are four tests for this project. To try out the test, go to the Test_data_generation directory

    Three tests that experiments the delay time of the timestamping are within test_time_delay.py, one test that experiments the gas usage of the batch timestamping feature is inside code test_gasUsage.py

    For details of test description and test results, please refer to the dissertation report and the comments within the code.

    Before executing any tests, make sure that the test parameters are checked and confirmed (Mainly the number of timestamping requests), they are marked with comment.

    After executing any test, the result data will be written to text files named correspondingly to the tests.

    To visualise the test results, please execute the data_analyser.py to see graph plots.

