#!/usr/bin/env python3
"""
BSC Wallet Streamlit GUI
Web interface for BSC Testnet wallet operations
"""

import streamlit as st
import json
import time
from bsc_wallet.bsc_wallet import BSCWallet
from bsc_wallet.config import SAMPLE_TOKENS, BSC_TESTNET_EXPLORER

# Page config
st.set_page_config(
    page_title="BSC Testnet Wallet",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = None
if 'bsc_wallet' not in st.session_state:
    st.session_state.bsc_wallet = BSCWallet()

def display_wallet_info(wallet_info):
    """Display wallet information in a nice format"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Wallet Information")
        st.text_area("Mnemonic Phrase", wallet_info['mnemonic'], height=80)
        st.text_input("Address", wallet_info['address'], disabled=True)
        st.text_input("BIP44 Path", wallet_info['bip44_path'], disabled=True)
    
    with col2:
        st.subheader("🔑 Keys")
        st.text_area("Private Key", wallet_info['private_key'], height=80)
        st.text_area("Public Key", wallet_info['public_key'], height=80)
        
        # QR Code placeholder
        st.info("💡 **Important:** Store your mnemonic and private key securely!")

def main():
    # Title and header
    st.title("💰 BSC Testnet Wallet")
    st.markdown("---")
    
    # Initialize current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    
    # Sidebar for navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose Operation",
        ["🏠 Home", "🆕 Generate Wallet", "📥 Import Wallet", "💰 Check Balances", 
         "🚀 Send BNB", "🪙 Send Tokens", "ℹ️ Network Info"],
        index=["🏠 Home", "🆕 Generate Wallet", "📥 Import Wallet", "💰 Check Balances", 
               "🚀 Send BNB", "🪙 Send Tokens", "ℹ️ Network Info"].index(st.session_state.current_page)
    )
    
    # Update session state when selectbox changes
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
    
    # Home Page
    if page == "🏠 Home":
        st.header("Welcome to BSC Testnet Wallet")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🆕 Generate")
            st.write("Create a new wallet with BIP39 mnemonic")
            if st.button("Generate New Wallet", type="primary"):
                # Navigate to Generate Wallet page
                st.session_state.current_page = "🆕 Generate Wallet"
                st.rerun()
        
        with col2:
            st.subheader("📥 Import")
            st.write("Import existing wallet from mnemonic or private key")
            if st.button("Import Wallet"):
                # Navigate to Import Wallet page
                st.session_state.current_page = "📥 Import Wallet"
                st.rerun()
        
        with col3:
            st.subheader("🔗 Network")
            st.write("BSC Testnet connection status")
            try:
                network_info = st.session_state.bsc_wallet.get_network_info()
                st.success(f"✅ Connected to Block #{network_info['latest_block']}")
            except Exception as e:
                st.error(f"❌ Connection failed: {e}")
        
        # Network Information
        st.markdown("---")
        st.subheader("🌐 Network Information")
        
        try:
            network_info = st.session_state.bsc_wallet.get_network_info()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Chain ID", network_info['chain_id'])
            with col2:
                st.metric("Latest Block", f"{network_info['latest_block']:,}")
            with col3:
                st.metric("Gas Price", f"{network_info['gas_price_gwei']:.2f} gwei")
            with col4:
                st.metric("Status", "🟢 Connected" if network_info['connected'] else "🔴 Disconnected")
            
            st.info(f"🔍 **Explorer:** {network_info['explorer_url']}")
            
        except Exception as e:
            st.error(f"Failed to get network info: {e}")
    
    # Generate Wallet Page
    elif page == "🆕 Generate Wallet":
        st.header("🆕 Generate New Wallet")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Settings")
            strength = st.selectbox(
                "Mnemonic Strength",
                [128, 256],
                format_func=lambda x: f"{x} bits ({'12' if x == 128 else '24'} words)"
            )
            
            if st.button("🎲 Generate Wallet", type="primary"):
                with st.spinner("Generating wallet..."):
                    try:
                        wallet_info = st.session_state.bsc_wallet.create_new_wallet(strength)
                        st.session_state.wallet = wallet_info
                        st.success("✅ Wallet generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error generating wallet: {e}")
        
        if st.session_state.wallet:
            with col2:
                display_wallet_info(st.session_state.wallet)
    
    # Import Wallet Page
    elif page == "📥 Import Wallet":
        st.header("📥 Import Wallet")
        
        import_method = st.radio(
            "Import Method",
            ["From Mnemonic", "From Private Key"]
        )
        
        if import_method == "From Mnemonic":
            st.subheader("Import from Mnemonic Phrase")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                mnemonic = st.text_area(
                    "Mnemonic Phrase",
                    placeholder="Enter your 12 or 24 word mnemonic phrase...",
                    height=100
                )
                
                account_index = st.number_input(
                    "Account Index (BIP44)",
                    min_value=0,
                    value=0
                )
                
                if st.button("📥 Import from Mnemonic", type="primary") and mnemonic:
                    with st.spinner("Importing wallet..."):
                        try:
                            wallet_info = st.session_state.bsc_wallet.import_wallet_from_mnemonic(
                                mnemonic.strip(), account_index
                            )
                            st.session_state.wallet = wallet_info
                            st.success("✅ Wallet imported successfully!")
                        except Exception as e:
                            st.error(f"❌ Error importing wallet: {e}")
            
            if st.session_state.wallet:
                with col2:
                    display_wallet_info(st.session_state.wallet)
        
        else:  # From Private Key
            st.subheader("Import from Private Key")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                private_key = st.text_input(
                    "Private Key",
                    type="password",
                    placeholder="Enter your private key (hex)..."
                )
                
                if st.button("🔑 Import from Private Key", type="primary") and private_key:
                    with st.spinner("Importing wallet..."):
                        try:
                            wallet_info = st.session_state.bsc_wallet.import_wallet_from_private_key(
                                private_key.strip()
                            )
                            st.session_state.wallet = wallet_info
                            st.success("✅ Wallet imported successfully!")
                        except Exception as e:
                            st.error(f"❌ Error importing wallet: {e}")
            
            if st.session_state.wallet:
                with col2:
                    st.subheader("🔐 Imported Wallet")
                    st.text_input("Address", st.session_state.wallet['address'], disabled=True)
                    st.text_area("Public Key", st.session_state.wallet['public_key'], height=80)
    
    # Check Balances Page
    elif page == "💰 Check Balances":
        st.header("💰 Check Balances")
        
        address = st.text_input(
            "Wallet Address",
            placeholder="Enter wallet address to check balances...",
            value=st.session_state.wallet['address'] if st.session_state.wallet else ""
        )
        
        if st.button("🔍 Check Balances", type="primary") and address:
            with st.spinner("Checking balances..."):
                try:
                    # BNB Balance
                    st.subheader("🟡 BNB Balance")
                    bnb_balance = st.session_state.bsc_wallet.get_bnb_balance(address)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("BNB Balance", f"{bnb_balance['balance_bnb']:.6f} BNB")
                    with col2:
                        st.metric("Balance (Wei)", f"{bnb_balance['balance_wei']:,}")
                    
                    # Token Balances
                    st.subheader("🪙 Token Balances")
                    
                    if SAMPLE_TOKENS:
                        for token_symbol, token_address in SAMPLE_TOKENS.items():
                            try:
                                token_balance = st.session_state.bsc_wallet.get_token_balance(
                                    token_address, address
                                )
                                
                                # Use actual token name from contract instead of symbol
                                actual_token_name = token_balance['token_name']
                                
                                with st.expander(f"{actual_token_name}"):
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Token", token_balance['token_symbol'])
                                    with col2:
                                        st.metric("Balance", f"{token_balance['balance_formatted']:.6f}")
                                    with col3:
                                        st.metric("Decimals", token_balance['decimals'])
                                    
                                    st.code(f"Token Address: {token_balance['token_address']}")
                                    
                            except Exception as e:
                                st.warning(f"Could not get {token_symbol} balance: {e}")
                    else:
                        st.info("No sample tokens configured")
                        
                except Exception as e:
                    st.error(f"❌ Error checking balances: {e}")
    
    # Send BNB Page
    elif page == "🚀 Send BNB":
        st.header("🚀 Send BNB")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Transaction Details")
            
            private_key = st.text_input(
                "Private Key",
                type="password",
                placeholder="Enter your private key...",
                value=st.session_state.wallet['private_key'] if st.session_state.wallet else ""
            )
            
            to_address = st.text_input(
                "Recipient Address",
                placeholder="Enter recipient address..."
            )
            
            amount = st.number_input(
                "Amount (BNB)",
                min_value=0.0,
                step=0.001,
                format="%.6f"
            )
            
            wait_confirmation = st.checkbox("Wait for confirmation", value=True)
            
            # Initialize confirmation state
            if 'bnb_confirm_pending' not in st.session_state:
                st.session_state.bnb_confirm_pending = False
            if 'bnb_tx_data' not in st.session_state:
                st.session_state.bnb_tx_data = {}
            
            if st.button("🚀 Send BNB", type="primary") and private_key and to_address and amount > 0:
                # Store transaction data in session state
                st.session_state.bnb_tx_data = {
                    'private_key': private_key,
                    'to_address': to_address,
                    'amount': amount,
                    'wait_confirmation': wait_confirmation
                }
                st.session_state.bnb_confirm_pending = True
                st.rerun()
            
            # Show confirmation dialog if pending
            if st.session_state.bnb_confirm_pending:
                st.warning(f"⚠️ You are about to send **{st.session_state.bnb_tx_data['amount']} BNB** to **{st.session_state.bnb_tx_data['to_address']}**")
                
                col_confirm, col_cancel = st.columns(2)
                
                with col_confirm:
                    if st.button("✅ Confirm Transaction", type="primary"):
                        with st.spinner("Sending transaction..."):
                            try:
                                result = st.session_state.bsc_wallet.send_bnb(
                                    st.session_state.bnb_tx_data['private_key'], 
                                    st.session_state.bnb_tx_data['to_address'], 
                                    st.session_state.bnb_tx_data['amount'], 
                                    st.session_state.bnb_tx_data['wait_confirmation']
                                )
                                
                                st.success("✅ Transaction sent successfully!")
                                
                                with col2:
                                    st.subheader("📄 Transaction Receipt")
                                    st.text_input("Transaction Hash", result['tx_hash'])
                                    st.text_input("From", result['from_address'])
                                    st.text_input("To", result['to_address'])
                                    st.text_input("Amount", f"{result['amount_bnb']} BNB")
                                    
                                    if 'status' in result:
                                        st.text_input("Status", result['status'])
                                        st.text_input("Gas Used", result.get('gas_used', 'N/A'))
                                    
                                    st.markdown(f"🔍 [View on Explorer]({result['explorer_url']})")
                                
                                # Reset confirmation state
                                st.session_state.bnb_confirm_pending = False
                                st.session_state.bnb_tx_data = {}
                                    
                            except Exception as e:
                                st.error(f"❌ Transaction failed: {e}")
                                # Reset confirmation state on error
                                st.session_state.bnb_confirm_pending = False
                                st.session_state.bnb_tx_data = {}
                
                with col_cancel:
                    if st.button("❌ Cancel", type="secondary"):
                        st.session_state.bnb_confirm_pending = False
                        st.session_state.bnb_tx_data = {}
                        st.rerun()
    
    # Send Tokens Page
    elif page == "🪙 Send Tokens":
        st.header("🪙 Send BEP-20 Tokens")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Transaction Details")
            
            private_key = st.text_input(
                "Private Key",
                type="password",
                placeholder="Enter your private key...",
                value=st.session_state.wallet['private_key'] if st.session_state.wallet else ""
            )
            
            # Token selection
            token_option = st.radio(
                "Token Selection",
                ["Sample Tokens", "Custom Token"]
            )
            
            if token_option == "Sample Tokens" and SAMPLE_TOKENS:
                token_name = st.selectbox("Select Token", list(SAMPLE_TOKENS.keys()))
                token_address = SAMPLE_TOKENS[token_name]
                st.code(f"Token Address: {token_address}")
            else:
                token_address = st.text_input(
                    "Token Contract Address",
                    placeholder="Enter token contract address..."
                )
            
            to_address = st.text_input(
                "Recipient Address",
                placeholder="Enter recipient address..."
            )
            
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=0.000001,
                format="%.6f"
            )
            
            wait_confirmation = st.checkbox("Wait for confirmation", value=True)
            
            # Get token info
            if token_address and st.button("ℹ️ Get Token Info"):
                try:
                    token_info = st.session_state.bsc_wallet.get_token_info(token_address)
                    st.info(f"Token: {token_info['name']} ({token_info['symbol']}) - {token_info['decimals']} decimals")
                except Exception as e:
                    st.warning(f"Could not get token info: {e}")
            
            # Initialize token confirmation state
            if 'token_confirm_pending' not in st.session_state:
                st.session_state.token_confirm_pending = False
            if 'token_tx_data' not in st.session_state:
                st.session_state.token_tx_data = {}
            
            if st.button("🪙 Send Tokens", type="primary") and private_key and token_address and to_address and amount > 0:
                # Store transaction data in session state
                st.session_state.token_tx_data = {
                    'private_key': private_key,
                    'token_address': token_address,
                    'to_address': to_address,
                    'amount': amount,
                    'wait_confirmation': wait_confirmation
                }
                st.session_state.token_confirm_pending = True
                st.rerun()
            
            # Show confirmation dialog if pending
            if st.session_state.token_confirm_pending:
                st.warning(f"⚠️ You are about to send **{st.session_state.token_tx_data['amount']} tokens** to **{st.session_state.token_tx_data['to_address']}**")
                
                col_confirm, col_cancel = st.columns(2)
                
                with col_confirm:
                    if st.button("✅ Confirm Token Transfer", type="primary"):
                        with st.spinner("Sending token transaction..."):
                            try:
                                result = st.session_state.bsc_wallet.send_token(
                                    st.session_state.token_tx_data['private_key'], 
                                    st.session_state.token_tx_data['token_address'], 
                                    st.session_state.token_tx_data['to_address'], 
                                    st.session_state.token_tx_data['amount'], 
                                    None, 
                                    st.session_state.token_tx_data['wait_confirmation']
                                )
                                
                                st.success("✅ Token transfer sent successfully!")
                                
                                with col2:
                                    st.subheader("📄 Transaction Receipt")
                                    st.text_input("Transaction Hash", result['tx_hash'])
                                    st.text_input("Token", f"{result['token_name']} ({result['token_symbol']})")
                                    st.text_input("From", result['from_address'])
                                    st.text_input("To", result['to_address'])
                                    st.text_input("Amount", f"{result['amount']} {result['token_symbol']}")
                                    
                                    if 'status' in result:
                                        st.text_input("Status", result['status'])
                                        st.text_input("Gas Used", result.get('gas_used', 'N/A'))
                                    
                                    st.markdown(f"🔍 [View on Explorer]({result['explorer_url']})")
                                
                                # Reset confirmation state
                                st.session_state.token_confirm_pending = False
                                st.session_state.token_tx_data = {}
                                    
                            except Exception as e:
                                st.error(f"❌ Token transfer failed: {e}")
                                # Reset confirmation state on error
                                st.session_state.token_confirm_pending = False
                                st.session_state.token_tx_data = {}
                
                with col_cancel:
                    if st.button("❌ Cancel Token Transfer", type="secondary"):
                        st.session_state.token_confirm_pending = False
                        st.session_state.token_tx_data = {}
                        st.rerun()
    
    # Network Info Page
    elif page == "ℹ️ Network Info":
        st.header("ℹ️ Network Information")
        
        try:
            network_info = st.session_state.bsc_wallet.get_network_info()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌐 Network Status")
                st.metric("Connection", "🟢 Connected" if network_info['connected'] else "🔴 Disconnected")
                st.metric("Chain ID", network_info['chain_id'])
                st.metric("Latest Block", f"{network_info['latest_block']:,}")
                st.metric("Gas Price", f"{network_info['gas_price_gwei']:.2f} gwei")
            
            with col2:
                st.subheader("🔗 Links")
                st.markdown(f"**Explorer:** [BSCScan Testnet]({network_info['explorer_url']})")
                st.markdown("**Faucet:** [BSC Testnet Faucet](https://testnet.binance.org/faucet-smart)")
                st.markdown("**RPC URL:** `https://data-seed-prebsc-1-s1.binance.org:8545/`")
            
            # Sample tokens
            st.subheader("🪙 Sample Token Addresses")
            if SAMPLE_TOKENS:
                for name, address in SAMPLE_TOKENS.items():
                    st.code(f"{name}: {address}")
            else:
                st.info("No sample tokens configured")
            
            # Transaction lookup
            st.subheader("🔍 Transaction Lookup")
            tx_hash = st.text_input("Transaction Hash", placeholder="Enter transaction hash...")
            
            if st.button("🔍 Check Transaction") and tx_hash:
                try:
                    tx_info = st.session_state.bsc_wallet.get_transaction_status(tx_hash)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Status", tx_info['status'])
                        if tx_info.get('block_number'):
                            st.metric("Block Number", tx_info['block_number'])
                    
                    with col2:
                        if tx_info.get('gas_used'):
                            st.metric("Gas Used", f"{tx_info['gas_used']:,}")
                        st.markdown(f"🔍 [View on Explorer]({tx_info['explorer_url']})")
                        
                except Exception as e:
                    st.error(f"Error checking transaction: {e}")
                    
        except Exception as e:
            st.error(f"Failed to get network info: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "🔗 **BSC Testnet Wallet** | Built with Streamlit | "
        f"[Explorer]({BSC_TESTNET_EXPLORER}) | "
        "[Faucet](https://testnet.binance.org/faucet-smart)"
    )

if __name__ == "__main__":
    main() 