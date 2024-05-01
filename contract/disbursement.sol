// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract DisbursementToken is Initializable, ERC20Upgradeable, ERC20PausableUpgradeable, AccessControlUpgradeable, UUPSUpgradeable {
    // Role definitions
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    // State definitions for disbursement
    enum DisbursementState { Created, InProgress, Completed, Paused }
    DisbursementState public state;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address defaultAdmin, address pauser, address minter, address upgrader)
        public initializer
    {
        __ERC20_init("DisbursementToken", "DTK");
        __ERC20Pausable_init();
        __AccessControl_init();
        __UUPSUpgradeable_init();

        _grantRole(DEFAULT_ADMIN_ROLE, defaultAdmin);
        _grantRole(PAUSER_ROLE, pauser);
        _grantRole(MINTER_ROLE, minter);
        _grantRole(UPGRADER_ROLE, upgrader);

        state = DisbursementState.Created; // Initial state
    }

    function pause() public onlyRole(PAUSER_ROLE) {
        require(state == DisbursementState.InProgress, "Can only pause when in progress");
        _pause();
        state = DisbursementState.Paused;
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        require(state == DisbursementState.Paused, "Can only unpause when paused");
        _unpause();
        state = DisbursementState.InProgress;
    }

    function mint(address to, uint256 amount) public onlyRole(MINTER_ROLE) {
        require(state == DisbursementState.Created || state == DisbursementState.InProgress, "Cannot mint in current state");
        _mint(to, amount);
        state = DisbursementState.Completed; // Change state after successful mint
    }

    function startDisbursement() public onlyRole(DEFAULT_ADMIN_ROLE) {
        require(state == DisbursementState.Created, "Disbursement already started or completed");
        state = DisbursementState.InProgress;
    }

    function completeDisbursement() public onlyRole(DEFAULT_ADMIN_ROLE) {
        require(state == DisbursementState.InProgress, "Disbursement must be in progress to complete");
        state = DisbursementState.Completed;
    }

    function resetDisbursement() public onlyRole(DEFAULT_ADMIN_ROLE) {
        require(state == DisbursementState.Completed, "Can only reset after completion");
        state = DisbursementState.Created; // Reset state to allow new disbursement
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        override onlyRole(UPGRADER_ROLE)
    {}

    // Override to maintain pausable state
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20Upgradeable, ERC20PausableUpgradeable)
    {
        super._update(from, to, value);
    }
}
