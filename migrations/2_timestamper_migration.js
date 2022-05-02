const Timestamper = artifacts.require("Timestamper");

module.exports = async function(deployer) 
{
    // deployment steps
    await deployer.deploy(Timestamper);

};