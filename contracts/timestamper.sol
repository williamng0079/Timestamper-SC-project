// SPDX-License-Identifier: MIT

// The MIT license declared (SPDX, 2018) specifies the following: 
// "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
// to deal in the Software without restriction."


pragma solidity >=0.4.22 <0.9.0;    //This specifies a range of solidity compilier versions that are accepted to compile this smart contract (Solidity, n.d.).

//import "hardhat/console.sol";
import "@openzeppelin/contracts/access/Ownable.sol";    //Only the address of the deployer can call functions tagged with onlyOwner within this smart contract (OpenZeppelin, n.d.).
//import "@openzeppelin/upgrades-core/contracts/Initializable.sol";   


contract Timestamper is Ownable                                     
{
    //uint256 private _hash;                            //Declare a private string variable _hash used to store the user input hash.
                                                        //Private variable means that accessing and modifying the information by other contracts are prevented (Solidity, n.d.). 
    event Timestamp(string indexed hash);               //Declareing an event allows arguments to be stored in the transaction's log, this is the main method of storing the user hash input onto the blockchain.
                                                        //"indexed" flag allows the respective arguments to be displayed in log (Solidity, n.d.). 
    
    //Memory and calldata define the data area where a variable is stored. 
    //It is used to temporarily store variables and their values (Solidity, n.d.).
    //calldata method is choosen choosen due to lower gas usage after testing both options.
    function timestamp(string calldata hash) public onlyOwner       
    {
        //_hash = hash;                                             
        //console.log("Timestamping:", hash);                       
                    
        emit Timestamp(hash);                           
        //This allows the argument (supplied hash input) event indexed to be logged in the transaction's input field (Solidity, n.d.).      
        
    }
    

    //This function takes a list of strings as input rather than a single string,
    //the for loop will iterate through the list of input and emit an event log for every single element inside the list
    //the keccak256 value of each input element will be assigned with a log index to be displayed on the event log page of the node providers.
    function batchTimestamp(string[] calldata hash) public onlyOwner 
    {
        for (uint256 i = 0; i < hash.length; i++) 
        {
            emit Timestamp(hash[i]);
        }
    }
}