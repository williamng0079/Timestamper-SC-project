# truffle
test local environment setup


1. npm

2. web3.js
    npm install web3 -g

3. node.js

4. truffle
    npm install truffle -g

    truffle set up

    cd into an empty directory
    truffle init 


5. ganache GUI

    linking to ganache: network config within truffle-config.js 
    import truffle-config.js to ganache gui


test network setup (later)

Reconfigure truffle-config.js to the Ropsten testnet


dependencies:

1. openzepplelin/contracts:
    npm i @openzepplelin/contracts
    
2. openzeppelin, upgradeable contract plugin
    npm install --save-dev @openzeppelin/truffle-upgrades

3. hardhat    
    npm install --save-dev hardhat

done...

1.  Timestamper smart contract created with the base functionality 
2.  deployed and tested on a local private ethereum network (ganache)


todo and ideas (avoid overscoping the project)...

run more simulations with the blocktime modified
input sanitisation 
mode selection 
make unittests
examine gas usage 
batch timestamp test


if time allows....
have a program where it stores user input in a database and queries such database each time to check if the hash existed already
front end stuff


prepare test scenarios

1.  a normal scenario
2.  test scripts for submitting a large number of hash in a short period
3.  testnet deployment Rinkeby (POA)/ Ropsten (PoW) eth network 
4.  
5.  


