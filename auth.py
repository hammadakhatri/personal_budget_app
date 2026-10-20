"""
Authentication module for OAuth and user management
"""
import streamlit as st
from sqlalchemy.orm import Session
from models import User
from db_operations.core import set_user_context

def get_or_create_user(db: Session, email: str, name: str, provider: str, sub: str) -> User:
    """Get existing user or create new one from OAuth login"""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        user = User(
            email=email,
            name=name,
            oauth_provider=provider,
            oauth_sub=sub
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user

def is_user_logged_in() -> bool:
    """Check if user is logged in via OAuth"""
    try:
        # Check if st.user has email attribute (indicates logged in)
        return hasattr(st.user, 'email') and st.user.email is not None
    except:
        return False

def require_auth(db: Session) -> User:
    """
    Require authentication and return current user.
    Shows login button if not authenticated.
    """
    if not is_user_logged_in():
        st.warning("🔒 Please log in to access the Budget App")
        if st.button("🔐 Login with Google", type="primary", use_container_width=True):
            st.login("google")
        st.stop()
    
    # Get or create user from OAuth info
    user = get_or_create_user(
        db,
        email=st.user.email,
        name=st.user.name or st.user.email.split('@')[0],
        provider="google",
        sub=st.user.sub
    )
    
    # Set user context for RLS
    set_user_context(db, user.id)
    
    return user

def get_current_user(db: Session) -> User | None:
    """Get current user without requiring auth (returns None if not logged in)"""
    if not is_user_logged_in():
        return None
    
    user = db.query(User).filter(User.email == st.user.email).first()
    if user:
        set_user_context(db, user.id)
    
    return user
