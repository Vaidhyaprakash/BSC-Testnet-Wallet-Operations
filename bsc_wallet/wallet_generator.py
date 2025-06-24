"""
Wallet Generation Module
Handles BIP39 mnemonic generation and BIP44 key derivation for BSC Testnet
"""

import logging
from typing import Dict, Tuple
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_account import Account
from .config import BIP44_PATH

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WalletGenerator:
    """
    Handles wallet generation from mnemonic phrases using BIP39/BIP44 standards
    """
    
    def __init__(self):
        self.mnemo = Mnemonic("english")
    
    def generate_mnemonic(self, strength: int = 128) -> str:
        """
        Generate a new mnemonic phrase
        
        Args:
            strength: Entropy strength in bits (128 = 12 words, 256 = 24 words)
            
        Returns:
            str: Generated mnemonic phrase
        """
        try:
            mnemonic = self.mnemo.generate(strength=strength)
            logger.info(f"Generated new mnemonic with {len(mnemonic.split())} words")
            return mnemonic
        except Exception as e:
            logger.error(f"Error generating mnemonic: {e}")
            raise
    
    def validate_mnemonic(self, mnemonic: str) -> bool:
        """
        Validate a mnemonic phrase
        
        Args:
            mnemonic: Mnemonic phrase to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            return self.mnemo.check(mnemonic)
        except Exception as e:
            logger.error(f"Error validating mnemonic: {e}")
            return False
    
    def derive_wallet_from_mnemonic(self, mnemonic: str, account_index: int = 0) -> Dict[str, str]:
        """
        Derive wallet keys and address from mnemonic using BIP44 standard
        
        Args:
            mnemonic: BIP39 mnemonic phrase
            account_index: Account index for BIP44 path (default: 0)
            
        Returns:
            Dict containing mnemonic, private_key, public_key, and address
        """
        try:
            if not self.validate_mnemonic(mnemonic):
                raise ValueError("Invalid mnemonic phrase")
            
            # Generate seed from mnemonic
            seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
            
            # Use BIP44 for Ethereum (BSC is Ethereum-compatible)
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(account_index)
            bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
            bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)
            
            # Get private key
            private_key_bytes = bip44_addr_ctx.PrivateKey().Raw().ToBytes()
            private_key_hex = private_key_bytes.hex()
            
            # Create account from private key
            account = Account.from_key(private_key_hex)
            
            # Get public key
            public_key = account._key_obj.public_key.to_hex()
            
            wallet_info = {
                "mnemonic": mnemonic,
                "private_key": private_key_hex,
                "public_key": public_key,
                "address": account.address,
                "bip44_path": f"m/44'/60'/0'/0/{account_index}"
            }
            
            logger.info(f"Successfully derived wallet for address: {account.address}")
            return wallet_info
            
        except Exception as e:
            logger.error(f"Error deriving wallet from mnemonic: {e}")
            raise
    
    def create_new_wallet(self, strength: int = 128) -> Dict[str, str]:
        """
        Create a completely new wallet with generated mnemonic
        
        Args:
            strength: Entropy strength in bits (128 = 12 words, 256 = 24 words)
        
        Returns:
            Dict containing all wallet information
        """
        try:
            mnemonic = self.generate_mnemonic(strength)
            return self.derive_wallet_from_mnemonic(mnemonic)
        except Exception as e:
            logger.error(f"Error creating new wallet: {e}")
            raise
    
    def import_wallet_from_private_key(self, private_key: str) -> Dict[str, str]:
        """
        Import wallet from existing private key
        
        Args:
            private_key: Hexadecimal private key string
            
        Returns:
            Dict containing wallet information
        """
        try:
            # Remove '0x' prefix if present
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            # Create account from private key
            account = Account.from_key(private_key)
            
            # Get public key
            public_key = account._key_obj.public_key.to_hex()
            
            wallet_info = {
                "mnemonic": "N/A (imported from private key)",
                "private_key": private_key,
                "public_key": public_key,
                "address": account.address,
                "bip44_path": "N/A (imported from private key)"
            }
            
            logger.info(f"Successfully imported wallet for address: {account.address}")
            return wallet_info
            
        except Exception as e:
            logger.error(f"Error importing wallet from private key: {e}")
            raise


 