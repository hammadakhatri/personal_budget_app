from sqlalchemy.orm import Session
from models import Category, CategoryType, Transaction
import streamlit as st

def create_category(db: Session, user_id: int, name: str, type: CategoryType, parent_id: int = None):
    category = Category(user_id=user_id, name=name, type=type, parent_id=parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    get_categories.clear() # Invalidate cache
    return category

@st.cache_data(show_spinner=False)
def get_categories(_db: Session, type: CategoryType = None):
    # Note: Streamlit cache hashing integration for Session might be needed 
    # or rely on ignoring 'db' if we trust logic. 
    # For now, simplistic approach or skipping cache on raw session functions 
    # if it proves problematic, but we want speed.
    query = _db.query(Category)
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
    get_categories.clear()
    return True
