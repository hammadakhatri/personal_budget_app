import streamlit as st
from database import get_db
from models import TransactionType, CategoryType
from crud import get_accounts, get_major_categories, get_subcategories, add_transaction, transfer_funds
from styles import get_custom_css

st.set_page_config(page_title="Add Transaction", page_icon="📝")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("📝 New Transaction")

db = next(get_db())

# Transaction Type Selection
# using custom columns for a button-like feel or just radio
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
            from_account_name = st.selectbox("From Account", list(account_names.keys()))
        with col2:
            to_account_name = st.selectbox("To Account", list(account_names.keys()), index=1 if len(accounts) > 1 else 0)
        
        from_acc = [acc for acc in accounts if acc.name == from_account_name][0]
        to_acc = [acc for acc in accounts if acc.name == to_account_name][0]
        
        exchange_rate = 1.0
        if from_acc.currency != to_acc.currency:
            st.info(f"💱 Exchange Rate: 1 {from_acc.currency} = ? {to_acc.currency}")
            exchange_rate = st.number_input("Exchange Rate", value=1.0)
        
        if st.button("Submit Transfer", type="primary"):
            if from_account_name == to_account_name:
                st.error("Source and Destination accounts must be different.")
            else:
                transfer_funds(db, account_names[from_account_name], account_names[to_account_name], amount, exchange_rate, description, date)
                st.success("✅ Transfer Recorded Successfully!")

else: # Income / Expense
    st.markdown("### 📂 Categorization")
    col_acc, col_cat = st.columns(2)
    
    with col_acc:
        account_name = st.selectbox("Wallet", list(account_names.keys()))
    
    # Category Selection
    cat_type = CategoryType.INCOME if selected_type == "Income" else CategoryType.EXPENSE
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
    
    if st.button(f"Add {selected_type}", type="primary"):
        if not selected_cat_id:
            st.warning("Please select a category!")
        else:
            add_transaction(db, description, amount, TransactionType(selected_type), account_names[account_name], selected_cat_id, date)
            st.balloons()
            st.success(f"✅ {selected_type} Added!")

