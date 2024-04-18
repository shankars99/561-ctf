// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {EvilHackerWallet} from "@src/EvilHackerWallet.sol";

contract EvilHackerWalletTest is Test {
    EvilHackerWallet private hackerWallet;

    address public hacker_leader = address(0x1);
    address public hacker_right_man = address(0x2);
    address public hacker_bot = address(0x3);
    uint256 balance = 1 * 10 ** 18;
    function setUp() public {
        vm.prank(hacker_leader);
        hackerWallet = new EvilHackerWallet(hacker_bot);
        vm.deal(hacker_right_man, balance);
    }

    function test_setBalance() public {
        vm.prank(hacker_right_man);
        hackerWallet.deposit{value: balance}();

        assertEq(hackerWallet.balances(hacker_right_man), balance);
    }

    function test_withdrawBalance() public {
        vm.startPrank(hacker_right_man);
        hackerWallet.deposit{value: balance}();
        hackerWallet.withdraw();

        assertEq(hackerWallet.balances(hacker_right_man), 0);
    }
}
