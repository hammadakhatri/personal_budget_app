from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from database import Base

class TransactionType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"

class CategoryType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    oauth_provider = Column(String)  # 'google'
    oauth_sub = Column(String)  # OAuth subject ID
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    currency = Column(String) # USD, PKR, etc.
    balance = Column(Float, default=0.0)

    user = relationship("User", back_populates="accounts")
    transactions_as_sender = relationship("Transaction", foreign_keys="[Transaction.account_id]", back_populates="account")
    transactions_as_receiver = relationship("Transaction", foreign_keys="[Transaction.transfer_to_account_id]", back_populates="transfer_to_account")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    type = Column(Enum(CategoryType))
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=datetime.today)
    description = Column(String)
    amount = Column(Float)
    currency = Column(String)
    type = Column(Enum(TransactionType))
    
    # Relationships
    account_id = Column(Integer, ForeignKey("accounts.id")) # From Account / Main Account
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # Null for transfers
    
    # For Transfers
    transfer_to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    transfer_exchange_rate = Column(Float, default=1.0) # Rate = To / From. e.g. 1 USD -> 278 PKR. Rate = 278.

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", foreign_keys=[account_id], back_populates="transactions_as_sender")
    transfer_to_account = relationship("Account", foreign_keys=[transfer_to_account_id], back_populates="transactions_as_receiver")
    category = relationship("Category", back_populates="transactions")

