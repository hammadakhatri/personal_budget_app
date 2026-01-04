import streamlit as st
import pandas as pd
from database import get_db
from crud import get_accounts
from styles import get_custom_css

st.set_page_config(page_title="Budget Dashboard", layout="wide", page_icon="💸")

# Inject Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("💸 Dashboard")
st.markdown("Welcome back! Here is an overview of your finances.")

# Load Data
db = next(get_db())
accounts = get_accounts(db)

# Metric Placeholders in a nice container
with st.container():
    st.markdown("### Total Net Worth")
    col1, col2 = st.columns(2)

    # Calculate Total Balances by Currency
    pkr_balance = sum(acc.balance for acc in accounts if acc.currency == "PKR")
    usd_balance = sum(acc.balance for acc in accounts if acc.currency == "USD")

    col1.metric("🇵🇰 Total PKR", f"₨ {pkr_balance:,.2f}")
    col2.metric("🇺🇸 Total USD", f"$ {usd_balance:,.2f}")

st.markdown("---")

st.subheader("💳 Your Wallets")
if not accounts:
    st.info("No wallets found. Go to **Manage Wallets** to create one.")
else:
    # Custom Card Layout for Wallets
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

st.markdown("---")
st.info("💡 **Tip:** Use the sidebar to add transactions or manage your setup.")

