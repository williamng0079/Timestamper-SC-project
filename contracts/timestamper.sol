// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.4.22 <0.9.0;

import "hardhat/console.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/upgrades-core/contracts/Initializable.sol";

contract Timestamper is Ownable 
{
    string private _hash;

    event Timestamp(string indexed hash);

    function timestamp(string memory hash) public onlyOwner 
    {
        _hash = hash;

        console.log("Timestamping:", hash);
        
        emit Timestamp(hash);
    }

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