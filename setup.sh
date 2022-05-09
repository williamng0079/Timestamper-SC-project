#!/bin/bash

## Use "chmod +x setup_installation" to ensure that this script is executable
## Note that the set up time for node js may take a while

## This is a set up .sh script used to download all the required modules for this project
sudo apt-get update
sudo apt install curl

## Download the lastest stable version of node js (v16.x) and use npm to install truffle and the required packages
## The hdwallet provider module is required for contract deployment and interaction to the public ropsten testnet
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install web3 -g
sudo npm install truffle -g
sudo npm install @truffle/hdwallet-provider

## Download the non-standard python libraries 
sudo pip3 install web3
sudo pip3 install python-dotenv
sudo pip3 install pyfiglet


## Display version of downloaded packages
echo $(truffle version)
echo node version: $(node --version)
echo npm version: $(npm --version)
