from sqlalchemy.orm import Session
from models import Transaction, TransactionType, Account
from datetime import datetime
from db_operations.accounts import update_account_balance
import streamlit as st

def add_transaction(db: Session, user_id: int, description: str, amount: float, type: TransactionType, 
                   account_id: int, category_id: int = None, date: datetime = None):
    if date is None:
        date = datetime.today()
        
    transaction = Transaction(
        user_id=user_id,
        description=description,
        amount=amount,
        type=type,
        account_id=account_id,
        category_id=category_id,
        date=date,
        currency=db.query(Account.currency).filter(Account.id == account_id).scalar()
    )
    db.add(transaction)
    
    # Update Balance
    if type == TransactionType.INCOME:
        update_account_balance(db, account_id, amount)
    elif type == TransactionType.EXPENSE:
        update_account_balance(db, account_id, -amount)
        
    db.commit()
    db.refresh(transaction)
    # Clear caches that might depend on transactions
    # Ideally we clear analytics cache here
    st.cache_data.clear() 
    return transaction

def transfer_funds(db: Session, user_id: int, from_account_id: int, to_account_id: int, amount: float, 
                  exchange_rate: float = 1.0, description: str = "Transfer", date: datetime = None):
    if date is None:
        date = datetime.today()

    from_acc = db.query(Account).filter(Account.id == from_account_id).first()
    
    transaction = Transaction(
        user_id=user_id,
        description=description,
        amount=amount,
        type=TransactionType.TRANSFER,
        account_id=from_account_id,
        transfer_to_account_id=to_account_id,
        transfer_exchange_rate=exchange_rate,
        date=date,
        currency=from_acc.currency
    )
    db.add(transaction)
    
    # Deduct from Source
    update_account_balance(db, from_account_id, -amount)
    # Add to Destination
    converted_amount = amount * exchange_rate
    update_account_balance(db, to_account_id, converted_amount)
    
    db.commit()
    db.refresh(transaction)
    st.cache_data.clear()
    return transaction

def get_transactions(db: Session, account_id: int = None, limit: int = None):
    """Get transactions, optionally filtered by account"""
    query = db.query(Transaction).order_by(Transaction.date.desc())
    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    if limit:
        query = query.limit(limit)
    return query.all()

def delete_transaction(db: Session, transaction_id: int):
    """Delete a transaction and revert balance changes"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise ValueError("Transaction not found")
    
    # Revert balance changes
    if transaction.type == TransactionType.INCOME:
        update_account_balance(db, transaction.account_id, -transaction.amount)
    elif transaction.type == TransactionType.EXPENSE:
        update_account_balance(db, transaction.account_id, transaction.amount)
    elif transaction.type == TransactionType.TRANSFER:
        # Revert transfer
        update_account_balance(db, transaction.account_id, transaction.amount)
        converted_amount = transaction.amount * transaction.transfer_exchange_rate
        update_account_balance(db, transaction.transfer_to_account_id, -converted_amount)
    
    db.delete(transaction)
    db.commit()
    st.cache_data.clear()
    return True
