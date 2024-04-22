// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {EvilHackerWallet} from "@src/EvilHackerWallet.sol";
import {AttackContract} from "@src/Attack.sol";

contract EvilHackerWalletAttackTest is Test {
    EvilHackerWallet private hackerWallet;
    AttackContract private attackContract;

    address constant hacker_leader = 0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577;
    address constant hacker_right_hand =
        0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783;
    address constant hacker_bot = 0x5B0331ED799637DF524bbFC7943f112fB7354a86;
    address constant hero = 0xd5DA4652E012e5629A3491616cC89F4E7339bA05;

    uint256 balance = 1 * 10 ** 18;
    function setUp() public {
        vm.prank(hacker_leader);
        hackerWallet = new EvilHackerWallet();

        vm.prank(hero);
        attackContract = new AttackContract(address(hackerWallet));

        vm.deal(hacker_leader, balance);
        vm.deal(hacker_right_hand, balance);
        vm.deal(hero, balance);
    }

    function test_reEntrancy() public {
        vm.prank(hacker_leader);
        hackerWallet.deposit{value: balance}();

        vm.prank(hacker_right_hand);
        hackerWallet.deposit{value: balance}();

        assertEq(hackerWallet.balances(hacker_leader), balance);
        assertEq(hackerWallet.balances(hacker_right_hand), balance);
        assertEq(hackerWallet.balances(hero), 0);

        assertEq(hackerWallet.getBalance(), balance * 2);

        vm.startPrank(hero);
        attackContract.attack{value: balance}();
        assertEq(attackContract.getBalance(), balance * 3);

        attackContract.withdraw();
        assertEq(hero.balance, balance * 3);
    }
}
