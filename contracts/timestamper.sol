// SPDX-License-Identifier: GPL-3.0-or-later 
// The GPL license declared specifies the following: Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed
// Source: https://spdx.org/licenses/GPL-3.0-or-later.html

pragma solidity >=0.4.22 <0.9.0;            //This line specifies a range of solidity compilier versions that are accepted to compile this smart contract

//import "hardhat/console.sol";
import "@openzeppelin/contracts/access/Ownable.sol";    
//import "@openzeppelin/upgrades-core/contracts/Initializable.sol";   //For contract upgradeability

//Only the address of the deployer can call functions tagged with onlyOwner within this smart contract.
contract Timestamper is Ownable                                     
{
    //uint256 private _hash;                                        //Declare a private string variable _hash used to store the user input hash.
                                                                    //Private variable means that other accessing and modifying the information by other contracts are prevented. (Source: https://docs.soliditylang.org/en/v0.4.24/contracts.html)
    event Timestamp(string indexed hash);                           //Declareing an event allows arguments to be stored in the transaction's log, this is the main method of storing the user hash input onto the blockchain
                                                                    //The Argument "indexed" allows the respective arguments to be searched for (Source:https://docs.soliditylang.org/en/v0.4.24/contracts.html#events)
    //Memory and calldata define the data area where a variable is stored. 
    //It is used to temporarily store variables and their values (Source:https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)
    //calldata choosen due to lower gas usage.
    function timestamp(string calldata hash) public onlyOwner       
    {
        //_hash = hash;                                             //Commented out for gas efficiency
        //console.log("Timestamping:", hash);                       //This is commented out to improve gas efficientcy
        emit Timestamp(hash);                                       //This allows the argument (supplied hash input) event indexed to be logged in the transaction's input field
    }
    
    function batchTimestamp(string[] calldata hash) public onlyOwner 
    {
        for (uint256 i = 0; i < hash.length; i++) 
        {
            emit Timestamp(hash[i]);
        }
    }
}