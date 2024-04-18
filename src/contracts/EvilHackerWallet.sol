// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract EvilHackerWallet {
    modifier onlyBot() {
        require(msg.sender == bot, "You are not the bot");
        _;
    }

    address private immutable bot;
    mapping(address => uint256) public balances;

    constructor(address _bot) {
        bot = _bot;
    }

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

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
