from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def get_total_net_worth(_db: Session):
    """
    Calculate total net worth grouped by currency using SQL.
    Returns: dict {currency: amount}
    """
    # Using raw SQL for speed and aggregation
    query = text("SELECT currency, SUM(balance) as total FROM accounts GROUP BY currency")
    result = _db.execute(query).fetchall()
    return {row[0]: row[1] for row in result}

@st.cache_data(show_spinner=False)
def get_income_expense_stats(_db: Session):
    """
    Get aggregated income vs expenses.
    """
    query = text("""
        SELECT type, SUM(amount) as total 
        FROM transactions 
        WHERE cast(type as text) IN ('Income', 'Expense') 
        GROUP BY type
    """)
    result = _db.execute(query).fetchall()
    df = pd.DataFrame(result, columns=["Type", "Amount"])
    return df

@st.cache_data(show_spinner=False)
def get_spending_by_category(_db: Session):
    """
    Get top spending categories (expenses only)
    """
    query = text("""
        SELECT c.name as category, SUM(t.amount) as amount 
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE cast(t.type as text) = 'Expense'
        GROUP BY c.name
        ORDER BY amount DESC
        LIMIT 5
    """)
    result = _db.execute(query).fetchall()
    return pd.DataFrame(result, columns=["Category", "Amount"])
