// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract EvilHackerDAO {
    modifier onlyBot() {
        require(msg.sender == bot, "You are not the bot");
        _;
    }

    address public owner;

    address constant leader = 0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577;
    address constant right_hand = 0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783;
    address constant bot = 0x5B0331ED799637DF524bbFC7943f112fB7354a86;
    address constant hero = 0xd5DA4652E012e5629A3491616cC89F4E7339bA05;

    mapping(address => uint256) public balances;
    address[] public hackers;
    uint256 public totalAmount = 100;

    constructor(address[] memory _hackers) {
        owner = leader;
        hackers = _hackers;
        hackers.push(msg.sender);

        balances[leader] = 49;
        balances[right_hand] = 45;
        balances[hero] = 6;
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

    function transfer(
        address _from,
        address _to,
        uint256 _amount
    ) external onlyBot {
        require(balances[_from] >= _amount, "Insufficient balance");
        balances[_from] -= _amount;
        balances[_to] += _amount;
    }

    function getHackerBalance(address _address) public view returns (uint256) {
        return balances[_address];
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
