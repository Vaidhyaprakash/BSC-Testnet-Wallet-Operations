"""
Main BSC Wallet Class
Combines wallet generation, BNB transfers, and token transfers
"""

import logging
from typing import Dict, Optional, List
from .wallet_generator import WalletGenerator
from .bnb_transfer import BNBTransfer
from .token_transfer import TokenTransfer
from .config import BSC_TESTNET_EXPLORER, SAMPLE_TOKENS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BSCWallet:
    """
    Main BSC Wallet class that provides complete wallet functionality
    """
    
    def __init__(self, rpc_url: Optional[str] = None):
        """
        Initialize BSC Wallet with all components
        
        Args:
            rpc_url: Custom RPC URL (optional)
        """
        try:
            self.wallet_generator = WalletGenerator()
            
            if rpc_url:
                self.bnb_transfer = BNBTransfer(rpc_url)
                self.token_transfer = TokenTransfer(rpc_url)
            else:
                self.bnb_transfer = BNBTransfer()
                self.token_transfer = TokenTransfer()
            
            logger.info("BSC Wallet initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing BSC Wallet: {e}")
            raise
    
    # Wallet Generation Methods
    def create_new_wallet(self, strength: int = 128) -> Dict[str, str]:
        """
        Create a new wallet with generated mnemonic
        
        Args:
            strength: Entropy strength in bits (128 = 12 words, 256 = 24 words)
        
        Returns:
            Dict containing wallet information
        """
        try:
            return self.wallet_generator.create_new_wallet(strength)
        except Exception as e:
            logger.error(f"Error creating new wallet: {e}")
            raise
    
    def import_wallet_from_mnemonic(self, mnemonic: str, account_index: int = 0) -> Dict[str, str]:
        """
        Import wallet from mnemonic phrase
        
        Args:
            mnemonic: BIP39 mnemonic phrase
            account_index: Account index for BIP44 derivation
            
        Returns:
            Dict containing wallet information
        """
        try:
            return self.wallet_generator.derive_wallet_from_mnemonic(mnemonic, account_index)
        except Exception as e:
            logger.error(f"Error importing wallet from mnemonic: {e}")
            raise
    
    def import_wallet_from_private_key(self, private_key: str) -> Dict[str, str]:
        """
        Import wallet from private key
        
        Args:
            private_key: Hexadecimal private key
            
        Returns:
            Dict containing wallet information
        """
        try:
            return self.wallet_generator.import_wallet_from_private_key(private_key)
        except Exception as e:
            logger.error(f"Error importing wallet from private key: {e}")
            raise
    
    # Balance Methods
    def get_bnb_balance(self, address: str) -> Dict[str, float]:
        """
        Get BNB balance for an address
        
        Args:
            address: Wallet address
            
        Returns:
            Dict with balance information
        """
        try:
            return self.bnb_transfer.get_balance(address)
        except Exception as e:
            logger.error(f"Error getting BNB balance: {e}")
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
            return self.token_transfer.get_token_balance(token_address, wallet_address, abi)
        except Exception as e:
            logger.error(f"Error getting token balance: {e}")
            raise
    
    def get_all_balances(self, wallet_address: str, token_addresses: List[str] = None) -> Dict:
        """
        Get all balances (BNB + tokens) for a wallet
        
        Args:
            wallet_address: Wallet address
            token_addresses: List of token contract addresses (optional)
            
        Returns:
            Dict with all balance information
        """
        try:
            result = {
                "wallet_address": wallet_address,
                "bnb_balance": None,
                "token_balances": {}
            }
            
            # Get BNB balance
            try:
                result["bnb_balance"] = self.get_bnb_balance(wallet_address)
            except Exception as e:
                logger.warning(f"Error getting BNB balance: {e}")
            
            # Get token balances
            if token_addresses:
                for token_address in token_addresses:
                    try:
                        token_balance = self.get_token_balance(token_address, wallet_address)
                        result["token_balances"][token_address] = token_balance
                    except Exception as e:
                        logger.warning(f"Error getting balance for token {token_address}: {e}")
            
            # Try sample tokens if no specific tokens provided
            elif SAMPLE_TOKENS:
                for token_name, token_address in SAMPLE_TOKENS.items():
                    try:
                        token_balance = self.get_token_balance(token_address, wallet_address)
                        result["token_balances"][token_name] = token_balance
                    except Exception as e:
                        logger.warning(f"Error getting balance for {token_name}: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting all balances: {e}")
            raise
    

    
    # Transfer Methods
    def send_bnb(self, private_key: str, to_address: str, amount_bnb: float, 
                 wait_for_confirmation: bool = True) -> Dict:
        """
        Send BNB to another address
        
        Args:
            private_key: Sender's private key
            to_address: Recipient address
            amount_bnb: Amount in BNB to send
            wait_for_confirmation: Whether to wait for confirmation
            
        Returns:
            Transaction result
        """
        try:
            return self.bnb_transfer.send_bnb(private_key, to_address, amount_bnb, wait_for_confirmation)
        except Exception as e:
            logger.error(f"Error sending BNB: {e}")
            raise
    
    def send_token(self, private_key: str, token_address: str, to_address: str, 
                   amount: float, abi: list = None, wait_for_confirmation: bool = True) -> Dict:
        """
        Send BEP-20 tokens to another address
        
        Args:
            private_key: Sender's private key
            token_address: Token contract address
            to_address: Recipient address
            amount: Amount of tokens to send
            abi: Token ABI (optional)
            wait_for_confirmation: Whether to wait for confirmation
            
        Returns:
            Transaction result
        """
        try:
            return self.token_transfer.send_token(
                private_key, token_address, to_address, amount, abi, wait_for_confirmation
            )
        except Exception as e:
            logger.error(f"Error sending token: {e}")
            raise
    
    # Utility Methods
    def get_token_info(self, token_address: str, abi: list = None) -> Dict:
        """
        Get token information
        
        Args:
            token_address: Token contract address
            abi: Token ABI (optional)
            
        Returns:
            Dict with token information
        """
        try:
            return self.token_transfer.get_token_info(token_address, abi)
        except Exception as e:
            logger.error(f"Error getting token info: {e}")
            raise
    
    def validate_address(self, address: str) -> bool:
        """
        Validate if an address is valid
        
        Args:
            address: Address to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            return self.bnb_transfer.web3.is_address(address)
        except Exception as e:
            logger.error(f"Error validating address: {e}")
            return False
    
    def get_network_info(self) -> Dict:
        """
        Get network information
        
        Returns:
            Dict with network information
        """
        try:
            return {
                "connected": self.bnb_transfer.web3.is_connected(),
                "chain_id": self.bnb_transfer.chain_id,
                "latest_block": self.bnb_transfer.web3.eth.block_number,
                "gas_price_wei": self.bnb_transfer.estimate_gas_price(),
                "gas_price_gwei": self.bnb_transfer.web3.from_wei(
                    self.bnb_transfer.estimate_gas_price(), 'gwei'
                ),
                "explorer_url": BSC_TESTNET_EXPLORER
            }
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            raise
    
    def get_transaction_status(self, tx_hash: str) -> Dict:
        """
        Get transaction status and information
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Dict with transaction information
        """
        try:
            # Try to get transaction receipt
            try:
                receipt = self.bnb_transfer.web3.eth.get_transaction_receipt(tx_hash)
                status = "Success" if receipt.status == 1 else "Failed"
                
                return {
                    "tx_hash": tx_hash,
                    "status": status,
                    "block_number": receipt.blockNumber,
                    "gas_used": receipt.gasUsed,
                    "explorer_url": f"{BSC_TESTNET_EXPLORER}/tx/{tx_hash}"
                }
            except Exception:
                # Transaction might be pending
                try:
                    tx = self.bnb_transfer.web3.eth.get_transaction(tx_hash)
                    return {
                        "tx_hash": tx_hash,
                        "status": "Pending",
                        "block_number": tx.blockNumber if tx.blockNumber else None,
                        "explorer_url": f"{BSC_TESTNET_EXPLORER}/tx/{tx_hash}"
                    }
                except Exception:
                    return {
                        "tx_hash": tx_hash,
                        "status": "Not Found",
                        "explorer_url": f"{BSC_TESTNET_EXPLORER}/tx/{tx_hash}"
                    }
                    
        except Exception as e:
            logger.error(f"Error getting transaction status: {e}")
            raise


 