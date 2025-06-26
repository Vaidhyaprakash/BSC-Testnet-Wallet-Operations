# BSC Testnet Wallet - Web Interface

A modern, user-friendly web application for BSC Testnet wallet operations built with Streamlit. Generate wallets, check balances, and send BNB/tokens with an intuitive graphical interface.

 ## 📦 Installation

### Prerequisites
- Python 3.13.4
- pip package manager

### Quick Setup

1. **Clone the Repository**
```bash
git clone <repository-url>
cd BSC-Testnet-Wallet-Operations
```

2. **Create Virtual Environment**
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux  
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Launch the Web Application**
```bash
streamlit run streamlit_app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Web3.py](https://img.shields.io/badge/web3.py-6.11+-green.svg)](https://web3py.readthedocs.io/)

## 🎯 Features

### 🔐 Wallet Operations
- **Generate New Wallets**: Create BIP39 mnemonic phrases with 12 or 24 words (128/256-bit entropy)
- **Import Wallets**: Import from mnemonic phrase or private key
- **Secure Display**: Safe viewing of wallet information with copy-paste functionality

### 💸 Transaction Management  
- **BNB Transfers**: Send native BNB with real-time confirmation
- **Token Transfers**: Send BEP-20 tokens with sample token support
- **Transaction Confirmation**: Optional wait for blockchain confirmation
- **Explorer Integration**: Direct links to BSCScan testnet explorer

### 💰 Balance Checking
- **BNB Balance**: Real-time BNB balance checking
- **Token Balances**: Support for multiple BEP-20 tokens
- **Sample Tokens**: Pre-configured USDT and BUSD testnet tokens

### 🌐 Network Information
- **Network Status**: Real-time BSC testnet connection status
- **Gas Price**: Current network gas price monitoring
- **Block Information**: Latest block number tracking
- **Transaction Lookup**: Check transaction status by hash

## 🖥️ Screenshots

### Home Dashboard
- Network status overview
- Quick navigation to all features
- Real-time connection monitoring

### Wallet Generation
- Choice between 12-word and 24-word mnemonics  
- Secure display of private keys and addresses

### Transaction Interface
- User-friendly send forms
- Confirmation dialogs with transaction details
- Loading states with progress indication
- Transaction receipts with explorer links

## 🚀 Getting Started

### 1. 🆕 Generate Your First Wallet
- Navigate to **"🆕 Generate Wallet"** page
- Choose mnemonic strength (12 or 24 words)
- Click **"🎲 Generate Wallet"**
- **Important**: Save your mnemonic phrase securely!

### 2. 💰 Get Testnet BNB
Your new wallet needs testnet BNB for transactions:
- Copy your wallet address
- Visit [BSC Testnet Faucet](https://testnet.binance.org/faucet-smart)
- Request testnet BNB (usually 0.1-1 BNB per request)

### 3. ✅ Check Your Balance
- Go to **"💰 Check Balances"** page  
- Enter your wallet address
- View BNB and token balances

### 4. 🚀 Send Your First Transaction
- Navigate to **"🚀 Send BNB"** or **"🪙 Send Tokens"**
- Enter your private key and transaction details
- Confirm the transaction
- Watch the loading indicator during processing
- View transaction receipt with explorer link

## 🏗️ Project Structure

```
BSC-Testnet-Wallet-Operations/
├── streamlit_app.py           # Main Streamlit web application
├── bsc_wallet/                # Core wallet functionality
│   ├── __init__.py           # Package initialization  
│   ├── config.py             # Network and token configuration
│   ├── bsc_wallet.py         # Main wallet API class
│   ├── wallet_generator.py   # BIP39/BIP44 wallet generation
│   ├── bnb_transfer.py       # Native BNB transfer operations
│   └── token_transfer.py     # BEP-20 token transfer operations
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup configuration
└── README.md                 # This documentation
```

## ⚙️ Configuration

### Network Settings
- **Network**: BSC Testnet
- **Chain ID**: 97
- **RPC URL**: `https://data-seed-prebsc-1-s1.binance.org:8545/`
- **Explorer**: `https://testnet.bscscan.com`

### Sample Tokens
Pre-configured testnet tokens for easy testing:
```python
SAMPLE_TOKENS = {
    "USDT": "0xA11c8D9DC9b66E209Ef60F0C8D969D3CD988782c",
    "BUSD": "0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee"
}
```

## 🎨 User Interface Features

### 🧭 Navigation Sidebar
- **🏠 Home**: Dashboard and network overview
- **🆕 Generate Wallet**: Create new wallets  
- **📥 Import Wallet**: Import existing wallets
- **💰 Check Balances**: View account balances
- **🚀 Send BNB**: Native BNB transfers
- **🪙 Send Tokens**: BEP-20 token transfers  
- **ℹ️ Network Info**: Network status and tools

### 🔄 Transaction Flow
1. **Form Input**: User-friendly forms with validation
2. **Confirmation Dialog**: Review transaction details
3. **Loading State**: Visual progress indicators  
4. **Result Display**: Success/error messages with receipts
5. **Reset State**: Clean interface ready for next transaction

### 🎯 Smart Features
- **Auto-filled Addresses**: Use generated wallet addresses automatically
- **Balance Validation**: Check sufficient funds before transactions
- **Gas Estimation**: Automatic gas price detection
- **Error Handling**: Clear, helpful error messages
- **Responsive Design**: Works on desktop and mobile browsers

## 🛡️ Security Best Practices

### 🔒 Wallet Security
- **Never share private keys** or mnemonic phrases
- **This is testnet only** - never use mainnet private keys
- **Store securely** - Use secure password managers for keys
- **Regular backups** - Keep multiple secure copies of mnemonics

### 🧪 Testnet Guidelines  
- **Testnet only**: This application only works with BSC Testnet
- **No real value**: Testnet tokens have no monetary value
- **Educational purpose**: For learning and development only
- **Faucet usage**: Get testnet BNB from official faucets

## 🔍 Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Insufficient funds" | No testnet BNB | Get BNB from [faucet](https://testnet.binance.org/faucet-smart) |
| "Connection failed" | Network issues | Check internet connection, try refreshing |
| "Invalid private key" | Wrong key format | Ensure 64-character hex string |
| "Transaction failed" | Various blockchain issues | Check gas fees, recipient address |
| Loading stuck | High network traffic | Wait longer or refresh page |

### 🆘 Getting Help

1. **Check Network Status**: Use the "ℹ️ Network Info" page
2. **Verify Balance**: Ensure sufficient testnet BNB for gas fees  
3. **Check Explorer**: Use transaction lookup to check status
4. **Refresh Application**: Sometimes a simple refresh helps
5. **Check Console**: Browser developer tools may show errors