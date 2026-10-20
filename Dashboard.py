import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_operations.core import get_db
from db_operations.accounts import get_accounts
from db_operations.transactions import get_transactions
from db_operations.analytics import (
    get_total_net_worth, 
    get_income_expense_stats, 
    get_spending_by_category
)
from models import TransactionType
from styles import get_custom_css
from auth import require_auth

st.set_page_config(page_title="Budget Dashboard", layout="wide", page_icon="💸", initial_sidebar_state="expanded")

# Check authentication first
db = next(get_db())
user = require_auth(db)

# Mobile view toggle
if 'mobile_view' not in st.session_state:
    st.session_state.mobile_view = False

# Add toggle in sidebar
with st.sidebar:
    st.markdown(f"### 👤 {user.name}")
    st.markdown(f"*{user.email}*")
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.logout()
    
    st.markdown("---")
    if st.button("📱 Toggle Mobile View" if not st.session_state.mobile_view else "💻 Toggle Desktop View", use_container_width=True):
        st.session_state.mobile_view = not st.session_state.mobile_view
        st.rerun()

# Rename the page in sidebar
st.sidebar.markdown("## 💸 Dashboard")

# Inject Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Apply mobile view CSS if enabled
if st.session_state.mobile_view:
    st.markdown("""
        <style>
            .main .block-container {
                max-width: 480px !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            /* Stack columns vertically in mobile view */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 100% !important;
                max-width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

st.title("💸 Dashboard")
st.markdown(f"Welcome back, **{user.name}**! Here is an overview of your finances.")

# Load Data Efficiently
# Note: get_accounts is cached
accounts = get_accounts(db) 

# Metric Placeholders in a nice container
with st.container():
    st.markdown("### Total Net Worth")
    col1, col2 = st.columns(2)

    # Use optimized SQL aggregation
    net_worth_by_currency = get_total_net_worth(db) 
    
    # Safely get values, defaulting to 0
    pkr_balance = net_worth_by_currency.get("PKR", 0.0)
    usd_balance = net_worth_by_currency.get("USD", 0.0)

    # If None is returned by SUM, it might be None
    pkr_balance = pkr_balance if pkr_balance else 0.0
    usd_balance = usd_balance if usd_balance else 0.0

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

# Charts Section
# Use optimized analytics queries
income_expense_df = get_income_expense_stats(db)
top_spending_df = get_spending_by_category(db)

if not income_expense_df.empty:
    st.subheader("📊 Your Spending Habits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Income vs Expense comparison
        fig_comparison = go.Figure(data=[
            go.Bar(
                x=income_expense_df['Type'],
                y=income_expense_df['Amount'],
                marker_color=['#10b981' if t == 'Income' else '#ef4444' for t in income_expense_df['Type']],
                text=income_expense_df['Amount'].apply(lambda x: f"${x:,.2f}" if x else "$0"),
                textposition='auto',
            )
        ])
        fig_comparison.update_layout(
            title="Income vs Expenses",
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col2:
        # Top spending categories
        if not top_spending_df.empty:
             fig_categories = px.pie(
                top_spending_df,
                values='Amount',
                names='Category',
                title="Top 5 Spending Categories",
                hole=0.6,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
             fig_categories.update_traces(textposition='outside', textinfo='percent+label')
             fig_categories.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300,
                showlegend=False,
                font=dict(family="Inter, sans-serif")
            )
             st.plotly_chart(fig_categories, use_container_width=True)

st.markdown("---")

# Recent Transactions
# Still need to fetch individual records for the list
transactions = get_transactions(db, limit=10)

if transactions:
    st.subheader("📜 Recent Transactions")
    
    for txn in transactions:
        if txn.type == TransactionType.TRANSFER:
            icon = "🔄"
            amount_str = f"{txn.amount:,.2f} {txn.currency}"
            category_text = f"Transfer to {txn.transfer_to_account.name if txn.transfer_to_account else 'Unknown'}"
            type_class = "transfer"
        elif txn.type == TransactionType.INCOME:
            icon = "💰"
            amount_str = f"+{txn.amount:,.2f} {txn.currency}"
            category_text = txn.category.name if txn.category else "Uncategorized"
            type_class = "income"
        else:
            icon = "💸"
            amount_str = f"-{txn.amount:,.2f} {txn.currency}"
            category_text = txn.category.name if txn.category else "Uncategorized"
            type_class = "expense"
        
        st.markdown(
            f"""
            <div class="transaction-row">
                <div class="t-icon {type_class}">{icon}</div>
                <div class="t-details">
                    <div class="t-description">{txn.description}</div>
                    <div class="t-category">{category_text}</div>
                </div>
                <div class="t-date">{txn.date.strftime('%b %d')}</div>
                <div class="t-amount {type_class}">{amount_str}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.info("💡 **Tip:** Use the sidebar to add transactions or manage your setup.")
