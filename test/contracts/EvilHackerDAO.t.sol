// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {EvilHackerDAO} from "@src/EvilHackerDAO.sol";

contract EvilHackerDAOTest is Test {
    EvilHackerDAO private hackerDAO;

    address constant hacker_leader = 0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577;
    address constant hacker_right_hand =
        0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783;
    address constant hacker_bot = 0x5B0331ED799637DF524bbFC7943f112fB7354a86;
    address constant hero = 0xd5DA4652E012e5629A3491616cC89F4E7339bA05;

    uint256 constant totalAmount = 100;
    uint256 constant leaderAmount = 49;
    uint256 constant rightHandAmount = 45;
    uint256 constant heroAmount = 6;

    function setUp() public {
        vm.prank(hacker_leader);
        address[] memory hackers = new address[](1);
        hackers[0] = hacker_right_hand;
        hackerDAO = new EvilHackerDAO(hackers);
    }

    function test_setOwner() public {
        vm.prank(hacker_leader);
        hackerDAO.updateOwner();
        assertEq(hackerDAO.getOwner(), hacker_leader);
    }

    function test_notBotCannotTransfer() public {
        vm.expectRevert("You are not the bot");
        hackerDAO.transfer(hacker_leader, hacker_right_hand, 51);
    }

    function test_updateOwner() public {
        vm.prank(hacker_bot);

        uint256 token_moved = 5;

        hackerDAO.transfer(hacker_leader, hacker_right_hand, token_moved);

        assertEq(hackerDAO.balances(hacker_leader), leaderAmount - token_moved);
        assertEq(
            hackerDAO.balances(hacker_right_hand),
            rightHandAmount + token_moved
        );

        hackerDAO.updateOwner();
        assertEq(hackerDAO.getOwner(), hacker_right_hand);
    }
}
