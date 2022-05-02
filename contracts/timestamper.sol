// SPDX-License-Identifier: GPL-3.0-or-later 
// The GPL license declared specifies the following: Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed
// Source: https://spdx.org/licenses/GPL-3.0-or-later.html


pragma solidity >=0.4.22 <0.9.0;            //This line specifies a range of solidity compilier versions that are accepted to compile this smart contract

import "hardhat/console.sol";
import "@openzeppelin/contracts/access/Ownable.sol";    //Ownable module allows ownership of this contract, only the specified owner can call the timestamp functions
import "@openzeppelin/upgrades-core/contracts/Initializable.sol";   //For contract upgradeability

contract Timestamper is Ownable             
{
    string private _hash;                                           //Declare a private string variable _hash used to store the user input hash.
                                                                    //Private variable means that other accessing and modifying the information by other contracts are prevented. (Source: https://docs.soliditylang.org/en/v0.4.24/contracts.html)
    event Timestamp(string indexed hash);                           //Declareing an event allows arguments to be stored in the transaction's log, this is the main method of storing the user hash input onto the blockchain
                                                                    //The Argument "indexed" allows the respective arguments to be searched for (Source:https://docs.soliditylang.org/en/v0.4.24/contracts.html#events)
    
    //Memory defines the data area where a variable is stored, it is used to temporarily store variables and their values (Source:https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)
    
    function timestamp(string memory hash) public onlyOwner         
    {
        _hash = hash;

        console.log("Timestamping:", hash);                         
        
        emit Timestamp(hash);                                       //This allows the hash variable (that stores the hash input) indexed with event to be logged in the transaction
    }
    
    //The below function allows a call (zero gas usage) to display the most recent value stored in _hash 
    function retrieve() public view returns (string memory)         
    {
        return _hash;
    }

    //function batchTimestamp(string[] memory hashes) public onlyOwner {
        //for (string i = 0; i < hashes.length; i++) {
        //    emit Timestamp(hashes[i]);
        //}
    //}
}