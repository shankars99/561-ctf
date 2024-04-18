// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {EvilHackerDAO} from "@src/EvilHackerDAO.sol";

contract EvilHackerDAOTest is Test {
    EvilHackerDAO private hackerDAO;

    address public hacker_leader = address(0x1);
    address public hacker_right_man = address(0x2);
    address public hacker_bot = address(0x3);
    function setUp() public {
        vm.prank(hacker_leader);
        address[] memory hackers = new address[](1);
        hackers[0] = hacker_right_man;
        hackerDAO = new EvilHackerDAO(hackers, hacker_bot);
    }

    function test_setOwner() public {
        vm.prank(hacker_leader);
        hackerDAO.updateOwner();
        assertEq(hackerDAO.getOwner(), hacker_leader);
    }

    function test_notBotCannotTransfer() public {
        vm.expectRevert("You are not the bot");
        hackerDAO.transfer(hacker_leader, hacker_right_man, 51);
    }

    function test_updateOwner() public {
        vm.prank(hacker_bot);
        hackerDAO.transfer(hacker_leader, hacker_right_man, 51);

        assertEq(hackerDAO.balances(hacker_leader), 49);
        assertEq(hackerDAO.balances(hacker_right_man), 51);

        hackerDAO.updateOwner();
        assertEq(hackerDAO.getOwner(), hacker_right_man);
    }
}
