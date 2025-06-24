// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

contract Prakash is ERC20 {
    constructor(uint256 initialSupply) ERC20("Prakash", "IVP") {
        _mint(msg.sender, initialSupply * (10 ** uint256(decimals())));
    }
}