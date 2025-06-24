"""
Configuration settings for BSC Testnet wallet operations
"""

# BSC Testnet Configuration
BSC_TESTNET_RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"
BSC_TESTNET_CHAIN_ID = 97
BSC_TESTNET_EXPLORER = "https://testnet.bscscan.com"

# BSC Testnet Faucets
BSC_TESTNET_FAUCETS = [
    "https://testnet.bnbchain.org/faucet-smart",
    "https://testnet.binance.org/faucet-smart"
]

# BIP44 Derivation Path for BSC (Ethereum-compatible)
BIP44_PATH = "m/44'/60'/0'/0/0"

# Gas Settings
DEFAULT_GAS_LIMIT = 21000
TOKEN_TRANSFER_GAS_LIMIT = 100000
DEFAULT_GAS_PRICE = 20000000000  # 20 Gwei

# Standard ERC-20 ABI for BEP-20 tokens
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Sample BEP-20 Token Addresses on BSC Testnet
SAMPLE_TOKENS = {
    "USDT": "0xA11c8D9DC9b66E209Ef60F0C8D969D3CD988782c",  # Sample testnet USDT
    "BUSD": "0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee",  # Sample testnet BUSD
    "IVP": "0xf3eeCd4b52ef54c15EdF2d5eD525A2d200701041"     # Custom IVP token (Prakash)
} 