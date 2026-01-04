import streamlit as st
import pandas as pd
from database import get_db
from crud import create_account, get_accounts
from styles import get_custom_css

st.set_page_config(page_title="Manage Wallets", page_icon="👛")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("👛 Manage Wallets")
st.markdown("Create and view your accounts here.")

db = next(get_db())

# Create New Wallet Form
with st.container():
    st.subheader("Create New Wallet")
    with st.expander("➕ Add a new wallet", expanded=True):
        with st.form("create_wallet_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Wallet Name", placeholder="e.g., Cash, Chase Bank")
            with col2:
                currency = st.selectbox("Currency", ["PKR", "USD", "EUR", "GBP"])
            
            initial_balance = st.number_input("Initial Balance", min_value=0.0, step=100.0, format="%.2f")
            
            submitted = st.form_submit_button("Create Wallet", type="primary")
            if submitted:
                if name:
                    try:
                        create_account(db, name, currency, initial_balance)
                        st.balloons()
                        st.success(f"Wallet '{name}' created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating wallet: {e}")
                else:
                    st.error("Please enter a wallet name.")

# View Wallets as Cards
st.subheader("Your Active Wallets")
accounts = get_accounts(db)

if accounts:
    cols = st.columns(3)
    for idx, acc in enumerate(accounts):
        with cols[idx % 3]:
            card_class = "usd" if acc.currency == "USD" else "pkr"
            st.markdown(
                f"""
                <div class="wallet-card {card_class}">
                    <div class="wallet-currency">{acc.currency}</div>
                    <div class="wallet-name">{acc.name}</div>
                    <div class="wallet-balance">{acc.balance:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("No wallets found. Create one above!")

