// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract EvilHackerWallet {
    modifier onlyBot() {
        require(msg.sender == BOT, "You are not the bot");
        _;
    }

    address constant BOT = 0x5B0331ED799637DF524bbFC7943f112fB7354a86;
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 bal = balances[msg.sender];
        require(bal > 0);

        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send Ether");

        balances[msg.sender] = 0;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
