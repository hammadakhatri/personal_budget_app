import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_db
from crud import get_transactions, get_accounts, delete_transaction
from models import TransactionType
from styles import get_custom_css
from auth import require_auth

st.set_page_config(page_title="Transaction History", page_icon="📜")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("📜 Transaction History")
st.markdown("View and manage all your transactions.")

db = next(get_db())
user = require_auth(db)

# Filters
st.subheader("🔍 Filters")
col1, col2, col3 = st.columns(3)

with col1:
    accounts = get_accounts(db)
    account_options = ["All Wallets"] + [acc.name for acc in accounts]
    selected_account = st.selectbox("Wallet", account_options)

with col2:
    transaction_types = ["All Types"] + [t.value for t in TransactionType]
    selected_type = st.selectbox("Type", transaction_types)

with col3:
    date_range = st.selectbox("Date Range", ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"])

st.markdown("---")

# Get transactions
account_id = None
if selected_account != "All Wallets":
    account_id = next((acc.id for acc in accounts if acc.name == selected_account), None)

transactions = get_transactions(db, account_id=account_id)

# Apply filters
if selected_type != "All Types":
    transactions = [t for t in transactions if t.type.value == selected_type]

if date_range != "All Time":
    days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}
    cutoff_date = datetime.now().date() - timedelta(days=days_map[date_range])
    transactions = [t for t in transactions if t.date >= cutoff_date]

# Display transactions
st.subheader(f"📊 Transactions ({len(transactions)} found)")

if transactions:
    for txn in transactions:
        # Determine display details
        if txn.type == TransactionType.TRANSFER:
            from_acc = txn.account.name
            to_acc = txn.transfer_to_account.name if txn.transfer_to_account else "Unknown"
            category_display = f"Transfer: {from_acc} → {to_acc}"
            amount_display = f"{txn.amount:,.2f} {txn.currency}"
            color = "🔄"
        elif txn.type == TransactionType.INCOME:
            category_display = txn.category.name if txn.category else "Uncategorized"
            amount_display = f"+{txn.amount:,.2f} {txn.currency}"
            color = "💰"
        else:  # EXPENSE
            category_display = txn.category.name if txn.category else "Uncategorized"
            amount_display = f"-{txn.amount:,.2f} {txn.currency}"
            color = "💸"
        
        # Display transaction row
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 2, 2, 1])
        
        with col1:
            st.markdown(f"### {color}")
        with col2:
            st.markdown(f"**{txn.date}**")
        with col3:
            st.markdown(f"{txn.description}")
        with col4:
            st.markdown(f"*{category_display}*")
        with col5:
            st.markdown(f"**{amount_display}**")
        with col6:
            if st.button("🗑️", key=f"delete_txn_{txn.id}", help="Delete transaction"):
                try:
                    delete_transaction(db, txn.id)
                    st.success("Transaction deleted!")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
        
        st.markdown("---")
    
    # Export option
    st.markdown("### 📥 Export Data")
    export_data = []
    for txn in transactions:
        if txn.type == TransactionType.TRANSFER:
            category = f"Transfer to {txn.transfer_to_account.name if txn.transfer_to_account else 'Unknown'}"
        else:
            category = txn.category.name if txn.category else "Uncategorized"
        
        export_data.append({
            "Date": txn.date,
            "Type": txn.type.value,
            "Description": txn.description,
            "Category": category,
            "Amount": txn.amount,
            "Currency": txn.currency,
            "Wallet": txn.account.name
        })
    
    df = pd.DataFrame(export_data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
else:
    st.info("No transactions found matching your filters.")
