"""
BEP-20 Token Transfer Module
Handles BEP-20 (ERC-20) token transfers on BSC Testnet
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
    TOKEN_TRANSFER_GAS_LIMIT,
    DEFAULT_GAS_PRICE,
    BSC_TESTNET_EXPLORER,
    ERC20_ABI,
    SAMPLE_TOKENS
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TokenTransfer:
    """
    Handles BEP-20 token transfers on BSC Testnet
    """
    
    def __init__(self, rpc_url: str = BSC_TESTNET_RPC_URL):
        """
        Initialize token transfer handler
        
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
            logger.error(f"Error initializing token transfer: {e}")
            raise
    
    def get_token_contract(self, token_address: str, abi: list = None) -> object:
        """
        Get token contract instance
        
        Args:
            token_address: Token contract address
            abi: Token ABI (defaults to standard ERC-20)
            
        Returns:
            Web3 contract instance
        """
        try:
            if not self.web3.is_address(token_address):
                raise ValueError("Invalid token address format")
            
            # Use provided ABI or default ERC-20 ABI
            contract_abi = abi if abi else ERC20_ABI
            
            # Get contract instance
            checksum_address = self.web3.to_checksum_address(token_address)
            contract = self.web3.eth.contract(address=checksum_address, abi=contract_abi)
            
            logger.info(f"Token contract loaded: {checksum_address}")
            return contract
            
        except Exception as e:
            logger.error(f"Error getting token contract: {e}")
            raise
    
    def get_token_info(self, token_address: str, abi: list = None) -> Dict:
        """
        Get token basic information
        
        Args:
            token_address: Token contract address
            abi: Token ABI (optional)
            
        Returns:
            Dict with token information
        """
        try:
            contract = self.get_token_contract(token_address, abi)
            
            # Get token info
            try:
                name = contract.functions.name().call()
            except:
                name = "Unknown"
            
            try:
                symbol = contract.functions.symbol().call()
            except:
                symbol = "UNK"
            
            try:
                decimals = contract.functions.decimals().call()
            except:
                decimals = 18
            
            try:
                total_supply = contract.functions.totalSupply().call()
            except:
                total_supply = 0
            
            token_info = {
                "address": self.web3.to_checksum_address(token_address),
                "name": name,
                "symbol": symbol,
                "decimals": decimals,
                "total_supply": total_supply
            }
            
            logger.info(f"Token info: {name} ({symbol}) - {decimals} decimals")
            return token_info
            
        except Exception as e:
            logger.error(f"Error getting token info: {e}")
            raise
    
    def get_token_balance(self, token_address: str, wallet_address: str, abi: list = None) -> Dict:
        """
        Get token balance for a wallet
        
        Args:
            token_address: Token contract address
            wallet_address: Wallet address
            abi: Token ABI (optional)
            
        Returns:
            Dict with balance information
        """
        try:
            contract = self.get_token_contract(token_address, abi)
            token_info = self.get_token_info(token_address, abi)
            
            # Validate wallet address
            if not self.web3.is_address(wallet_address):
                raise ValueError("Invalid wallet address format")
            
            checksum_wallet = self.web3.to_checksum_address(wallet_address)
            
            # Get balance
            balance_raw = contract.functions.balanceOf(checksum_wallet).call()
            
            # Convert to human readable format
            decimals = token_info['decimals']
            balance_formatted = balance_raw / (10 ** decimals)
            
            result = {
                "wallet_address": checksum_wallet,
                "token_address": token_info['address'],
                "token_name": token_info['name'],
                "token_symbol": token_info['symbol'],
                "balance_raw": balance_raw,
                "balance_formatted": balance_formatted,
                "decimals": decimals
            }
            
            logger.info(f"Token balance: {balance_formatted} {token_info['symbol']} for {checksum_wallet}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting token balance: {e}")
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
    
    def create_token_transfer_transaction(self, token_address: str, from_address: str,
                                        to_address: str, amount: float, abi: list = None,
                                        gas_price: Optional[int] = None) -> Dict:
        """
        Create a token transfer transaction
        
        Args:
            token_address: Token contract address
            from_address: Sender address
            to_address: Recipient address
            amount: Amount of tokens to send (in human readable format)
            abi: Token ABI (optional)
            gas_price: Gas price in wei (optional)
            
        Returns:
            Transaction dictionary
        """
        try:
            contract = self.get_token_contract(token_address, abi)
            token_info = self.get_token_info(token_address, abi)
            
            # Validate addresses
            if not self.web3.is_address(from_address):
                raise ValueError("Invalid from_address format")
            if not self.web3.is_address(to_address):
                raise ValueError("Invalid to_address format")
            
            # Convert to checksum addresses
            from_checksum = self.web3.to_checksum_address(from_address)
            to_checksum = self.web3.to_checksum_address(to_address)
            
            # Convert amount to raw format (considering decimals)
            decimals = token_info['decimals']
            amount_raw = int(amount * (10 ** decimals))
            
            # Get gas price
            if gas_price is None:
                gas_price = self.estimate_gas_price()
            
            # Get nonce
            nonce = self.web3.eth.get_transaction_count(from_checksum)
            
            # Build transaction
            transaction = contract.functions.transfer(
                to_checksum,
                amount_raw
            ).build_transaction({
                'chainId': self.chain_id,
                'gas': TOKEN_TRANSFER_GAS_LIMIT,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            
            logger.info(f"Created token transfer: {amount} {token_info['symbol']} from {from_checksum} to {to_checksum}")
            return transaction
            
        except Exception as e:
            logger.error(f"Error creating token transfer transaction: {e}")
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
            
            logger.info("Token transfer transaction signed successfully")
            return signed_txn.rawTransaction.hex()
            
        except Exception as e:
            logger.error(f"Error signing token transfer transaction: {e}")
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
            
            logger.info(f"Token transfer transaction broadcasted with hash: {tx_hash_hex}")
            logger.info(f"View on BSC Testnet Explorer: {BSC_TESTNET_EXPLORER}/tx/{tx_hash_hex}")
            
            return tx_hash_hex
            
        except Exception as e:
            logger.error(f"Error broadcasting token transfer transaction: {e}")
            raise
    
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
            logger.info(f"Waiting for confirmation of token transfer: {tx_hash}")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                    if receipt:
                        status = "Success" if receipt.status == 1 else "Failed"
                        logger.info(f"Token transfer confirmed! Status: {status}")
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
            
            raise TimeoutError(f"Token transfer confirmation timeout after {timeout} seconds")
            
        except Exception as e:
            logger.error(f"Error waiting for token transfer confirmation: {e}")
            raise
    
    def send_token(self, private_key: str, token_address: str, to_address: str, 
                   amount: float, abi: list = None, wait_for_confirmation: bool = True) -> Dict:
        """
        Complete token transfer process
        
        Args:
            private_key: Sender's private key
            token_address: Token contract address
            to_address: Recipient address
            amount: Amount of tokens to send
            abi: Token ABI (optional)
            wait_for_confirmation: Whether to wait for confirmation
            
        Returns:
            Transaction result with hash, gas used, and status
        """
        try:
            # Get sender address
            account = Account.from_key(private_key)
            from_address = account.address
            
            # Get token info
            token_info = self.get_token_info(token_address, abi)
            
            logger.info(f"=== Token Transfer Process Started ===")
            logger.info(f"Token: {token_info['name']} ({token_info['symbol']})")
            logger.info(f"From: {from_address}")
            logger.info(f"To: {to_address}")
            logger.info(f"Amount: {amount} {token_info['symbol']}")
            
            # Check sender token balance
            balance_info = self.get_token_balance(token_address, from_address, abi)
            if balance_info['balance_formatted'] < amount:
                raise ValueError(f"Insufficient token balance. Available: {balance_info['balance_formatted']} {token_info['symbol']}")
            
            # Create transaction
            transaction = self.create_token_transfer_transaction(
                token_address, from_address, to_address, amount, abi
            )
            
            # Sign transaction
            signed_tx = self.sign_transaction(transaction, private_key)
            
            # Broadcast transaction
            tx_hash = self.broadcast_transaction(signed_tx)
            
            result = {
                "tx_hash": tx_hash,
                "from_address": from_address,
                "to_address": to_address,
                "token_address": token_info['address'],
                "token_name": token_info['name'],
                "token_symbol": token_info['symbol'],
                "amount": amount,
                "explorer_url": f"{BSC_TESTNET_EXPLORER}/tx/{tx_hash}"
            }
            
            # Wait for confirmation if requested
            if wait_for_confirmation:
                confirmation = self.wait_for_confirmation(tx_hash)
                result.update(confirmation)
            
            logger.info(f"=== Token Transfer Completed ===")
            return result
            
        except Exception as e:
            logger.error(f"Error in token transfer: {e}")
            raise


 