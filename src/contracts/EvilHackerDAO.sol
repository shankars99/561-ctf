// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract EvilHackerDAO {

    /**
     * @notice The onlyBot modifier
     * @dev Only a transaction from the address of the bot is allowed to execute the function
     */
    modifier onlyBot() {
        require(msg.sender == bot, "You are not the bot");
        _;
    }

    /**
     * @notice The list of users that are part of the DAO
     * @dev The same addresses from the .env file
     */
    address constant leader = 0xAef9c71b2d81efF1ddE720f57360e0B36c1C9577;
    address constant right_hand = 0x9a89279AA5Be0F7320ae2f650FCfc4AB9427B783;
    address constant hero = 0xd5DA4652E012e5629A3491616cC89F4E7339bA05;
    address constant bot = 0x5B0331ED799637DF524bbFC7943f112fB7354a86;

    /**
     * @notice The list of hackers in the DAO
     * @dev The hackers are the users of the contract
     * @return The list of hackers
     */
    address[] public hackers;

    /**
     * @notice The balances of the hackers
     * @dev The balance of a user is the number of tokens they have
     * @return The balance of the user
     */
    mapping(address => uint256) public balances;

    /**
     * @notice The owner of the contract
     * @dev The owner is the address with the most tokens
     * @return The address of the owner
     */
    address public owner;

    /**
     * @notice The total amount of tokens in supply
     * @dev The total amount of tokens in the contract
     * @return The total amount of tokens
     */
    uint256 public totalAmount = 100;

    /**
     * @notice The constructor of the contract
     * @param _hackers The list of hackers in the DAO
     * @dev The constructor initializes the contract with the list of hackers and the initial balances
     */
    constructor(address[] memory _hackers) {
        owner = leader;
        hackers = _hackers;
        hackers.push(msg.sender);

        balances[leader] = 49;
        balances[right_hand] = 45;
        balances[hero] = 6;
    }

    /**
     * @notice The function to update the owner of the contract
     * @dev The owner is the address with the most tokens
     */
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

    /**
     * @notice The function to transfer hacker tokens between hackers
     * @param _from The address of the sender
     * @param _to The address of the receiver
     * @param _amount The amount of tokens to transfer
     * @dev This function can only be called by the bot
     */
    function transfer(
        address _from,
        address _to,
        uint256 _amount
    ) external onlyBot {
        require(balances[_from] >= _amount, "Insufficient balance");
        balances[_from] -= _amount;
        balances[_to] += _amount;
    }

    /**
     * @notice The function to get the hacker token balance of a hacker
     * @param _address The address of the hacker
     * @return The balance of the hacker
     */
    function getHackerBalance(address _address) public view returns (uint256) {
        return balances[_address];
    }

    /**
     * @notice The function to get the owner of the contract
     * @return The address of the owner
     */
    function getOwner() public view returns (address) {
        return owner;
    }
}
