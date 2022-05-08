// Migrations are JavaScript files that help deploy contracts to the Ethereum network. 
// These files are responsible for staging deployment tasks, 
// and they're written under the assumption that deployment needs will change over time (Truffle, n.d.)

const Timestamper = artifacts.require("Timestamper");

module.exports = async function(deployer) 
{
    // deployment steps
    await deployer.deploy(Timestamper);

};