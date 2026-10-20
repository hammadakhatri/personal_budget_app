from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Account, Category, Transaction, TransactionType, CategoryType
from datetime import datetime

# --- Account Operations ---
def create_account(db: Session, user_id: int, name: str, currency: str, initial_balance: float = 0.0):
    account = Account(user_id=user_id, name=name, currency=currency, balance=initial_balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_accounts(db: Session):
    return db.query(Account).all()

def get_account_by_name(db: Session, name: str):
    return db.query(Account).filter(Account.name == name).first()

def update_account_balance(db: Session, account_id: int, amount: float):
    # amount can be negative
    account = db.query(Account).filter(Account.id == account_id).first()
    if account:
        account.balance += amount
        db.commit()
        db.refresh(account)

# --- Category Operations ---
def create_category(db: Session, user_id: int, name: str, type: CategoryType, parent_id: int = None):
    category = Category(user_id=user_id, name=name, type=type, parent_id=parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session, type: CategoryType = None):
    query = db.query(Category)
    if type:
        query = query.filter(Category.type == type)
    return query.all()

def get_major_categories(db: Session, type: CategoryType = None):
    query = db.query(Category).filter(Category.parent_id == None)
    if type:
        query = query.filter(Category.type == type)
    return query.all()

def get_subcategories(db: Session, parent_id: int):
    return db.query(Category).filter(Category.parent_id == parent_id).all()

# --- Transaction Operations ---
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
    return transaction

def transfer_funds(db: Session, user_id: int, from_account_id: int, to_account_id: int, amount: float, 
                  exchange_rate: float = 1.0, description: str = "Transfer", date: datetime = None):
    if date is None:
        date = datetime.today()

    # Create Transaction Record
    # We record it as a TRANSFER type.
    # convention: amount is what left the source account.
    
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
    
    # Update Balances
    # Deduct from Source
    update_account_balance(db, from_account_id, -amount)
    
    # Add to Destination (converted)
    converted_amount = amount * exchange_rate
    update_account_balance(db, to_account_id, converted_amount)
    
    db.commit()
    db.refresh(transaction)
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
    return True

def delete_category(db: Session, category_id: int):
    """Delete a category if it has no associated transactions"""
    # Check if category has transactions
    transaction_count = db.query(Transaction).filter(Transaction.category_id == category_id).count()
    if transaction_count > 0:
        raise ValueError(f"Cannot delete category: {transaction_count} transaction(s) are using this category")
    
    # Check if category has children
    children_count = db.query(Category).filter(Category.parent_id == category_id).count()
    if children_count > 0:
        raise ValueError(f"Cannot delete category: {children_count} sub-category(ies) exist under this category")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise ValueError("Category not found")
    
    db.delete(category)
    db.commit()
    return True

def delete_account(db: Session, account_id: int):
    """Delete an account if it has no associated transactions"""
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
    return True

