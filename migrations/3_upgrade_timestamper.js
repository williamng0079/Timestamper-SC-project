const { upgradeProxy } = require('@openzeppelin/truffle-upgrades');

const Timestamper = artifacts.require("Timestamper");

module.exports = async function(deployer) 
{
    // upgrade steps
    const existing = await Timestamper.deployed();
    await upgradeProxy(existing.address, Timestamper, { deployer });
};