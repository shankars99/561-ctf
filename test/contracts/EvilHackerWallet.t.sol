// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {EvilHackerWallet} from "@src/EvilHackerWallet.sol";

contract EvilHackerWalletTest is Test {
    EvilHackerWallet private hackerWallet;

    address constant hacker_leader = 0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577;
    address constant hacker_right_hand =
        0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783;
    address constant hacker_bot = 0x5B0331ED799637DF524bbFC7943f112fB7354a86;
    address constant hero = 0xd5DA4652E012e5629A3491616cC89F4E7339bA05;

    uint256 constant totalAmount = 100;
    uint256 constant leaderAmount = 49;
    uint256 constant rightHandAmount = 45;
    uint256 constant heroAmount = 6;

    uint256 balance = 1 * 10 ** 18;
    function setUp() public {
        vm.prank(hacker_leader);
        hackerWallet = new EvilHackerWallet(hacker_bot);
        vm.deal(hacker_right_hand, balance);
    }

    function test_setBalance() public {
        vm.prank(hacker_right_hand);
        hackerWallet.deposit{value: balance}();

        assertEq(hackerWallet.balances(hacker_right_hand), balance);
    }

    function test_withdrawBalance() public {
        vm.startPrank(hacker_right_hand);
        hackerWallet.deposit{value: balance}();
        hackerWallet.withdraw();

        assertEq(hackerWallet.balances(hacker_right_hand), 0);
    }
}
