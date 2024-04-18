// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {EvilHackerWallet} from "@src/EvilHackerWallet.sol";
import {AttackContract} from "@src/Attack.sol";

contract EvilHackerWalletAttackTest is Test {
    EvilHackerWallet private hackerWallet;
    AttackContract private attackContract;

    address public hacker_leader = address(0x1);
    address public hacker_right_man = address(0x2);
    address public hacker_bot = address(0x3);

    address public hero = address(0x4);

    uint256 balance = 1 * 10 ** 18;
    function setUp() public {
        vm.prank(hacker_leader);
        hackerWallet = new EvilHackerWallet(hacker_bot);

        vm.prank(hero);
        attackContract = new AttackContract(address(hackerWallet));

        vm.deal(hacker_leader, balance);
        vm.deal(hacker_right_man, balance);
        vm.deal(hero, balance);
    }

    function test_reEntrancy() public {
        vm.prank(hacker_leader);
        hackerWallet.deposit{value: balance}();

        vm.prank(hacker_right_man);
        hackerWallet.deposit{value: balance}();

        assertEq(hackerWallet.balances(hacker_leader), balance);
        assertEq(hackerWallet.balances(hacker_right_man), balance);
        assertEq(hackerWallet.balances(hero), 0);

        assertEq(hackerWallet.getBalance(), balance * 2);

        vm.startPrank(hero);
        attackContract.attack{value: balance}();
        assertEq(attackContract.getBalance(), balance * 3);

        attackContract.withdraw();
        assertEq(hero.balance, balance * 3);
    }
}
