"""
BNB Transfer Module
Handles native BNB transfers on BSC Testnet
"""

import logging
import time
from typing import Dict, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from .config import (
    BSC_TESTNET_RPC_URL, 
    BSC_TESTNET_CHAIN_ID, 
    DEFAULT_GAS_LIMIT, 
    DEFAULT_GAS_PRICE,
    BSC_TESTNET_EXPLORER,
    BSC_TESTNET_FAUCETS
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BNBTransfer:
    """
    Handles BNB transfers on BSC Testnet
    """
    
    def __init__(self, rpc_url: str = BSC_TESTNET_RPC_URL):
        """
        Initialize BNB transfer handler
        
        Args:
            rpc_url: BSC Testnet RPC URL
        """
        try:
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
            
            # Add POA middleware for BSC (Proof of Authority chain)
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            self.chain_id = BSC_TESTNET_CHAIN_ID
            
            if not self.web3.is_connected():
                raise ConnectionError("Failed to connect to BSC Testnet")
            
            logger.info(f"Connected to BSC Testnet: {rpc_url}")
            logger.info(f"Chain ID: {self.chain_id}")
            logger.info("POA middleware injected for BSC compatibility")
            
        except Exception as e:
            logger.error(f"Error initializing BNB transfer: {e}")
            raise
    
    def get_balance(self, address: str) -> Dict[str, float]:
        """
        Get BNB balance for an address
        
        Args:
            address: Wallet address
            
        Returns:
            Dict with balance in wei and BNB
        """
        try:
            # Validate address
            if not self.web3.is_address(address):
                raise ValueError("Invalid address format")
            
            # Convert to checksum address
            checksum_address = self.web3.to_checksum_address(address)
            
            # Get balance in wei
            balance_wei = self.web3.eth.get_balance(checksum_address)
            
            # Convert to BNB
            balance_bnb = self.web3.from_wei(balance_wei, 'ether')
            
            result = {
                "address": checksum_address,
                "balance_wei": balance_wei,
                "balance_bnb": float(balance_bnb)
            }
            
            logger.info(f"Balance for {checksum_address}: {balance_bnb} BNB")
            return result
            
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            raise
    
    def estimate_gas_price(self) -> int:
        """
        Get current gas price from the network
        
        Returns:
            Gas price in wei
        """
        try:
            gas_price = self.web3.eth.gas_price
            logger.info(f"Current gas price: {gas_price} wei ({self.web3.from_wei(gas_price, 'gwei')} gwei)")
            return gas_price
        except Exception as e:
            logger.warning(f"Error getting gas price, using default: {e}")
            return DEFAULT_GAS_PRICE
    
    def create_transaction(self, from_address: str, to_address: str, 
                         amount_bnb: float, gas_price: Optional[int] = None) -> Dict:
        """
        Create a BNB transfer transaction
        
        Args:
            from_address: Sender address
            to_address: Recipient address
            amount_bnb: Amount in BNB to send
            gas_price: Gas price in wei (optional)
            
        Returns:
            Transaction dictionary
        """
        try:
            # Validate addresses
            if not self.web3.is_address(from_address):
                raise ValueError("Invalid from_address format")
            if not self.web3.is_address(to_address):
                raise ValueError("Invalid to_address format")
            
            # Convert to checksum addresses
            from_checksum = self.web3.to_checksum_address(from_address)
            to_checksum = self.web3.to_checksum_address(to_address)
            
            # Convert amount to wei
            amount_wei = self.web3.to_wei(amount_bnb, 'ether')
            
            # Get gas price
            if gas_price is None:
                gas_price = self.estimate_gas_price()
            
            # Get nonce
            nonce = self.web3.eth.get_transaction_count(from_checksum)
            
            # Create transaction
            transaction = {
                'nonce': nonce,
                'to': to_checksum,
                'value': amount_wei,
                'gas': DEFAULT_GAS_LIMIT,
                'gasPrice': gas_price,
                'chainId': self.chain_id
            }
            
            logger.info(f"Created transaction: {amount_bnb} BNB from {from_checksum} to {to_checksum}")
            return transaction
            
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise
    
    def sign_transaction(self, transaction: Dict, private_key: str) -> str:
        """
        Sign a transaction with private key
        
        Args:
            transaction: Transaction dictionary
            private_key: Private key (hex string)
            
        Returns:
            Signed transaction (hex string)
        """
        try:
            # Remove '0x' prefix if present
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            # Sign transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)
            
            logger.info("Transaction signed successfully")
            return signed_txn.rawTransaction.hex()
            
        except Exception as e:
            logger.error(f"Error signing transaction: {e}")
            raise
    
    def broadcast_transaction(self, signed_transaction: str) -> str:
        """
        Broadcast signed transaction to the network
        
        Args:
            signed_transaction: Signed transaction (hex string)
            
        Returns:
            Transaction hash
        """
        try:
            # Send transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_transaction)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"Transaction broadcasted with hash: {tx_hash_hex}")
            logger.info(f"View on BSC Testnet Explorer: {BSC_TESTNET_EXPLORER}/tx/{tx_hash_hex}")
            
            return tx_hash_hex
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Provide more specific error messages
            if "insufficient funds" in error_str:
                raise ValueError("Insufficient funds: Your wallet doesn't have enough BNB to cover the transaction amount plus gas fees.")
            elif "nonce too low" in error_str:
                raise ValueError("Nonce too low: This transaction has already been processed or there's a nonce conflict.")
            elif "nonce too high" in error_str:
                raise ValueError("Nonce too high: Transaction nonce is higher than expected. Try again in a few seconds.")
            elif "gas price too low" in error_str:
                raise ValueError("Gas price too low: Current network gas price is higher than specified. Try increasing the gas price.")
            elif "intrinsic gas too low" in error_str:
                raise ValueError("Gas limit too low: The transaction requires more gas than specified.")
            elif "connection" in error_str or "timeout" in error_str:
                raise ConnectionError("Network connection issue: Unable to broadcast transaction. Check your internet connection or try a different RPC endpoint.")
            else:
                logger.error(f"Error broadcasting transaction: {e}")
                raise ValueError(f"Transaction broadcast failed: {e}")
    
    def wait_for_confirmation(self, tx_hash: str, timeout: int = 300) -> Dict:
        """
        Wait for transaction confirmation
        
        Args:
            tx_hash: Transaction hash
            timeout: Timeout in seconds
            
        Returns:
            Transaction receipt
        """
        try:
            logger.info(f"Waiting for confirmation of transaction: {tx_hash}")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                    if receipt:
                        status = "Success" if receipt.status == 1 else "Failed"
                        logger.info(f"Transaction confirmed! Status: {status}")
                        logger.info(f"Gas used: {receipt.gasUsed}")
                        logger.info(f"Block number: {receipt.blockNumber}")
                        
                        return {
                            "tx_hash": tx_hash,
                            "status": status,
                            "gas_used": receipt.gasUsed,
                            "block_number": receipt.blockNumber,
                            "confirmation_time": time.time() - start_time
                        }
                except Exception:
                    # Transaction not yet mined
                    pass
                
                time.sleep(2)  # Wait 2 seconds before checking again
            
            raise TimeoutError(f"Transaction confirmation timeout after {timeout} seconds")
            
        except Exception as e:
            logger.error(f"Error waiting for confirmation: {e}")
            raise
    
    def send_bnb(self, private_key: str, to_address: str, amount_bnb: float, 
                 wait_for_confirmation: bool = True) -> Dict:
        """
        Complete BNB transfer process
        
        Args:
            private_key: Sender's private key
            to_address: Recipient address
            amount_bnb: Amount in BNB to send
            wait_for_confirmation: Whether to wait for confirmation
            
        Returns:
            Transaction result with hash, gas used, and status
        """
        try:
            # Get sender address
            account = Account.from_key(private_key)
            from_address = account.address
            
            logger.info(f"=== BNB Transfer Process Started ===")
            logger.info(f"From: {from_address}")
            logger.info(f"To: {to_address}")
            logger.info(f"Amount: {amount_bnb} BNB")
            
            # Check sender balance
            balance_info = self.get_balance(from_address)
            if balance_info['balance_bnb'] < amount_bnb:
                error_msg = f"Insufficient balance. Available: {balance_info['balance_bnb']} BNB, Required: {amount_bnb} BNB"
                if balance_info['balance_bnb'] == 0:
                    error_msg += f"\n\n🚨 Your wallet has no testnet BNB!"
                    error_msg += f"\n\n💡 To get testnet BNB, visit one of these faucets:"
                    for faucet in BSC_TESTNET_FAUCETS:
                        error_msg += f"\n   • {faucet}"
                    error_msg += f"\n\n📍 Your wallet address: {from_address}"
                    error_msg += f"\n\n⏰ Faucets typically give 0.1-1 BNB per request and may have daily limits."
                raise ValueError(error_msg)
            
            # Create transaction
            transaction = self.create_transaction(from_address, to_address, amount_bnb)
            
            # Sign transaction
            signed_tx = self.sign_transaction(transaction, private_key)
            
            # Broadcast transaction
            tx_hash = self.broadcast_transaction(signed_tx)
            
            result = {
                "tx_hash": tx_hash,
                "from_address": from_address,
                "to_address": to_address,
                "amount_bnb": amount_bnb,
                "explorer_url": f"{BSC_TESTNET_EXPLORER}/tx/{tx_hash}"
            }
            
            # Wait for confirmation if requested
            if wait_for_confirmation:
                confirmation = self.wait_for_confirmation(tx_hash)
                result.update(confirmation)
            
            logger.info(f"=== BNB Transfer Completed ===")
            return result
            
        except Exception as e:
            logger.error(f"Error in BNB transfer: {e}")
            raise


 