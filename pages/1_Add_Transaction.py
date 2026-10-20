import streamlit as st
from db_operations.core import get_db
from models import TransactionType, CategoryType
from db_operations.accounts import get_accounts
from db_operations.categories import get_major_categories, get_subcategories
from db_operations.transactions import add_transaction, transfer_funds
from styles import get_custom_css
from auth import require_auth

st.set_page_config(page_title="Add Transaction", page_icon="📝")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("📝 New Transaction")

db = next(get_db())
user = require_auth(db)

# Transaction Type Selection
type_cols = st.columns(3)
selected_type = st.radio("Transaction Type", [t.value for t in TransactionType], horizontal=True, label_visibility="collapsed")

st.markdown("---")

# Common Fields Container
with st.container():
    col_date, col_amount = st.columns(2)
    with col_date:
        date = st.date_input("Date")
    with col_amount:
        amount = st.number_input("Amount", min_value=0.01, format="%.2f", help="Amount in Account's Currency")
    
    description = st.text_input("Description", placeholder="e.g. Grocery at Imtiaz, Freelance Payment...")

# Fetch Accounts
accounts = get_accounts(db)
account_names = {acc.name: acc.id for acc in accounts}

if not accounts:
    st.error("Please create a wallet first!")
    st.stop()

if selected_type == "Transfer":
    st.markdown("### 💱 Transfer Details")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            from_account_name = st.selectbox("From Wallet", list(account_names.keys()))
        with col2:
            to_account_name = st.selectbox("To Wallet", list(account_names.keys()), index=1 if len(accounts) > 1 else 0)
        
        from_acc = [acc for acc in accounts if acc.name == from_account_name][0]
        to_acc = [acc for acc in accounts if acc.name == to_account_name][0]
        
        # Display wallet currencies
        st.info(f"**Transfer**: {from_acc.name} ({from_acc.currency}) → {to_acc.name} ({to_acc.currency})")
        
        exchange_rate = 1.0
        transferred_amount = amount
        
        # Cross-currency transfer
        if from_acc.currency != to_acc.currency:
            st.markdown("#### 💱 Currency Conversion")
            
            # Option to enter either exchange rate or transferred amount
            conversion_method = st.radio(
                "How would you like to specify the conversion?",
                ["Enter Exchange Rate", "Enter Transferred Amount"],
                horizontal=True
            )
            
            col_a, col_b = st.columns(2)
            
            if conversion_method == "Enter Exchange Rate":
                with col_a:
                    exchange_rate = st.number_input(
                        f"Exchange Rate (1 {from_acc.currency} = ? {to_acc.currency})",
                        min_value=0.0001,
                        value=1.0,
                        step=0.01,
                        format="%.4f"
                    )
                with col_b:
                    transferred_amount = amount * exchange_rate
                    st.metric(
                        f"Amount Received ({to_acc.currency})",
                        f"{transferred_amount:,.2f}",
                        help="Calculated based on exchange rate"
                    )
            else:  # Enter Transferred Amount
                with col_a:
                    transferred_amount = st.number_input(
                        f"Amount Received ({to_acc.currency})",
                        min_value=0.01,
                        value=amount,
                        step=1.0,
                        format="%.2f"
                    )
                with col_b:
                    if amount > 0:
                        exchange_rate = transferred_amount / amount
                        st.metric(
                            f"Exchange Rate (1 {from_acc.currency})",
                            f"{exchange_rate:.4f} {to_acc.currency}",
                            help="Calculated based on amounts"
                        )
                    else:
                        st.warning("Enter amount to calculate exchange rate")
        else:
            # Same currency transfer
            st.success(f"✓ Same currency transfer - no conversion needed")
        
        if st.button("Submit Transfer", type="primary", use_container_width=True):
            if from_account_name == to_account_name:
                st.error("Source and Destination wallets must be different.")
            else:
                transfer_funds(db, user.id, account_names[from_account_name], account_names[to_account_name], amount, exchange_rate, description, date)
                st.toast("✅ Transfer Recorded Successfully!", icon="✅")

else: # Income / Expense
    st.markdown("### 📂 Categorization")
    col_acc, col_cat = st.columns(2)
    
    with col_acc:
        account_name = st.selectbox("Wallet", list(account_names.keys()))
    
    # Category Selection
    cat_type = CategoryType.INCOME if selected_type == "Income" else CategoryType.EXPENSE
    
    # Use cached getter
    major_categories = get_major_categories(db, cat_type)
    major_cat_names = {c.name: c.id for c in major_categories}
    
    with col_cat:
        major_cat_select = st.selectbox("Category", list(major_cat_names.keys()))
    
    selected_cat_id = None
    if major_cat_select:
        major_id = major_cat_names[major_cat_select]
        sub_categories = get_subcategories(db, major_id)
        if sub_categories:
            sub_cat_names = {c.name: c.id for c in sub_categories}
            sub_cat_select = st.selectbox("Sub-Category", list(sub_cat_names.keys()))
            selected_cat_id = sub_cat_names.get(sub_cat_select)
        else:
            selected_cat_id = major_id 
    
    if st.button(f"Add {selected_type}", type="primary", use_container_width=True):
        if not selected_cat_id:
            st.warning("Please select a category!")
        else:
            add_transaction(db, user.id, description, amount, TransactionType(selected_type), account_names[account_name], selected_cat_id, date)
            st.balloons()
            st.toast(f"✅ {selected_type} Added!", icon="🎉")

