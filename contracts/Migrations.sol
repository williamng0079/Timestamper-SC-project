// SPDX-License-Identifier: MIT

// Truffle requires a Migrations contract in order to use the migration scripts,
// the migration contract will be deployed initially as the first migration and won't be updated again (Consensys Software, n.d.).

pragma solidity >=0.4.22 <0.9.0;

contract Migrations {
  address public owner = msg.sender;
  uint public last_completed_migration;

  modifier restricted() {
    require(
      msg.sender == owner,
      "This function is restricted to the contract's owner"
    );
    _;
  }

  function setCompleted(uint completed) public restricted {
    last_completed_migration = completed;
  }
}
