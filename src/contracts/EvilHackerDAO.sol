// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract EvilHackerDAO {
    modifier onlyBot() {
        require(msg.sender == bot, "You are not the bot");
        _;
    }

    address private owner;
    address private immutable bot;
    mapping(address => uint256) public balances;
    address[] public hackers;
    uint256 public totalAmount = 100;

    constructor(address[] memory _hackers, address _bot) {
        owner = msg.sender;
        hackers = _hackers;
        hackers.push(msg.sender);

        balances[msg.sender] = totalAmount;
        bot = _bot;
    }

    function updateOwner() external {
        uint256 highestBalance = 0;
        address highestBalanceAddress;

        for (uint256 i = 0; i < hackers.length; i++) {
            if (balances[hackers[i]] > highestBalance) {
                highestBalance = balances[hackers[i]];
                highestBalanceAddress = hackers[i];
            }
        }

        owner = highestBalanceAddress;
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function transfer(
        address _from,
        address _to,
        uint256 _amount
    ) external onlyBot {
        require(balances[_from] >= _amount, "Insufficient balance");
        balances[_from] -= _amount;
        balances[_to] += _amount;
    }
}
