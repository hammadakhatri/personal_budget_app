import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import get_db
from crud import get_transactions, get_accounts
from models import TransactionType
from styles import get_custom_css
from auth import require_auth

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("📊 Financial Analytics")
st.markdown("Visualize your spending patterns and financial trends.")

db = next(get_db())
user = require_auth(db)

# Get all transactions
transactions = get_transactions(db)
accounts = get_accounts(db)

if not transactions:
    st.warning("No transactions found. Start adding transactions to see analytics!")
    st.stop()

# Prepare data
data = []
for txn in transactions:
    if txn.type == TransactionType.TRANSFER:
        continue  # Skip transfers for analytics
    
    data.append({
        "Date": txn.date,
        "Type": txn.type.value,
        "Amount": txn.amount,
        "Currency": txn.currency,
        "Category": txn.category.name if txn.category else "Uncategorized",
        "Wallet": txn.account.name,
        "Description": txn.description
    })

df = pd.DataFrame(data)

if df.empty:
    st.info("No income or expense transactions found for analysis.")
    st.stop()

# Convert date to datetime for better plotting
df['Date'] = pd.to_datetime(df['Date'])

# Time period selector
st.subheader("📅 Time Period")
period = st.selectbox("Select Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "All Time"])

if period != "All Time":
    days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90, "Last Year": 365}
    cutoff_date = datetime.now() - timedelta(days=days_map[period])
    df = df[df['Date'] >= cutoff_date]

st.markdown("---")

# Key Metrics
st.subheader("💡 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_income = df[df['Type'] == 'Income']['Amount'].sum()
total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
net_savings = total_income - total_expense
transaction_count = len(df)

with col1:
    st.metric("💰 Total Income", f"${total_income:,.2f}", delta=None)
with col2:
    st.metric("💸 Total Expenses", f"${total_expense:,.2f}", delta=None)
with col3:
    delta_color = "normal" if net_savings >= 0 else "inverse"
    st.metric("💵 Net Savings", f"${net_savings:,.2f}", delta=f"{net_savings:,.2f}")
with col4:
    st.metric("📝 Transactions", f"{transaction_count}")

st.markdown("---")

# Row 1: Income vs Expense Over Time + Spending by Category
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Income vs Expense Over Time")
    
    # Group by date and type
    time_df = df.groupby([df['Date'].dt.to_period('D').astype(str), 'Type'])['Amount'].sum().reset_index()
    time_df.columns = ['Date', 'Type', 'Amount']
    
    fig_time = px.line(
        time_df, 
        x='Date', 
        y='Amount', 
        color='Type',
        markers=True,
        color_discrete_map={'Income': '#10b981', 'Expense': '#ef4444'}
    )
    fig_time.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    st.subheader("🍰 Spending by Category")
    
    # Filter only expenses
    expense_df = df[df['Type'] == 'Expense']
    if not expense_df.empty:
        category_spending = expense_df.groupby('Category')['Amount'].sum().reset_index()
        category_spending = category_spending.sort_values('Amount', ascending=False)
        
        fig_pie = px.pie(
            category_spending,
            values='Amount',
            names='Category',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No expense data available.")

st.markdown("---")

# Row 2: Top Spending Categories + Monthly Trend
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Spending Categories")
    
    expense_df = df[df['Type'] == 'Expense']
    if not expense_df.empty:
        top_categories = expense_df.groupby('Category')['Amount'].sum().reset_index()
        top_categories = top_categories.sort_values('Amount', ascending=False).head(10)
        
        fig_bar = px.bar(
            top_categories,
            x='Amount',
            y='Category',
            orientation='h',
            color='Amount',
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(
            xaxis_title="Total Spent",
            yaxis_title="Category",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No expense data available.")

with col2:
    st.subheader("📅 Monthly Income vs Expense")
    
    # Group by month
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_df = df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
    
    fig_monthly = go.Figure()
    
    income_data = monthly_df[monthly_df['Type'] == 'Income']
    expense_data = monthly_df[monthly_df['Type'] == 'Expense']
    
    fig_monthly.add_trace(go.Bar(
        x=income_data['Month'],
        y=income_data['Amount'],
        name='Income',
        marker_color='#10b981'
    ))
    
    fig_monthly.add_trace(go.Bar(
        x=expense_data['Month'],
        y=expense_data['Amount'],
        name='Expense',
        marker_color='#ef4444'
    ))
    
    fig_monthly.update_layout(
        barmode='group',
        xaxis_title="Month",
        yaxis_title="Amount",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")

# Row 3: Wallet Distribution
st.subheader("💳 Current Wallet Distribution")

if accounts:
    wallet_data = []
    for acc in accounts:
        wallet_data.append({
            "Wallet": acc.name,
            "Balance": acc.balance,
            "Currency": acc.currency
        })
    
    wallet_df = pd.DataFrame(wallet_data)
    
    # Separate by currency
    col1, col2 = st.columns(2)
    
    with col1:
        pkr_wallets = wallet_df[wallet_df['Currency'] == 'PKR']
        if not pkr_wallets.empty:
            st.markdown("#### 🇵🇰 PKR Wallets")
            fig_pkr = px.bar(
                pkr_wallets,
                x='Wallet',
                y='Balance',
                color='Balance',
                color_continuous_scale='Greens'
            )
            fig_pkr.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_pkr, use_container_width=True)
    
    with col2:
        usd_wallets = wallet_df[wallet_df['Currency'] == 'USD']
        if not usd_wallets.empty:
            st.markdown("#### 🇺🇸 USD Wallets")
            fig_usd = px.bar(
                usd_wallets,
                x='Wallet',
                y='Balance',
                color='Balance',
                color_continuous_scale='Blues'
            )
            fig_usd.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_usd, use_container_width=True)

st.markdown("---")
st.info("💡 **Tip:** Use the filters above to analyze specific time periods and gain deeper insights into your spending habits!")
