from sqlalchemy.orm import Session
from models import Account
import streamlit as st

def create_account(db: Session, user_id: int, name: str, currency: str, initial_balance: float = 0.0):
    account = Account(user_id=user_id, name=name, currency=currency, balance=initial_balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    # Invalidate cache when data changes
    get_accounts.clear() 
    return account

@st.cache_data(show_spinner=False)
def get_accounts(_db: Session):
    """
    Fetch all accounts. Cached to prevent redundant DB calls.
    """
    return _db.query(Account).all()

def get_account_by_name(db: Session, name: str):
    return db.query(Account).filter(Account.name == name).first()

def update_account_balance(db: Session, account_id: int, amount: float):
    # amount can be negative
    account = db.query(Account).filter(Account.id == account_id).first()
    if account:
        account.balance += amount
        db.commit()
        db.refresh(account)
        get_accounts.clear() # Invalidate cache

def delete_account(db: Session, account_id: int):
    """Delete an account if it has no associated transactions"""
    from models import Transaction
    
    # Check if account has transactions
    transaction_count = db.query(Transaction).filter(
        (Transaction.account_id == account_id) | 
        (Transaction.transfer_to_account_id == account_id)
    ).count()
    
    if transaction_count > 0:
        raise ValueError(f"Cannot delete wallet: {transaction_count} transaction(s) are using this wallet")
    
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Wallet not found")
    
    db.delete(account)
    db.commit()
    get_accounts.clear()
    return True
