import streamlit as st
import pandas as pd
from db_operations.core import get_db
from models import CategoryType
from db_operations.categories import create_category, get_categories, get_major_categories, delete_category
from styles import get_custom_css
from auth import require_auth

st.set_page_config(page_title="Manage Categories", page_icon="🏷️")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("🏷️ Manage Categories")
st.markdown("Organize your finances with custom categories.")

db = next(get_db())
user = require_auth(db)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### New Major Category")
        with st.form("major_cat_form"):
            major_name = st.text_input("Name", placeholder="e.g. Utilities, Salary")
            major_type = st.selectbox("Type", ["Income", "Expense"])
            
            if st.form_submit_button("Create Major", type="primary"):
                if major_name:
                    create_category(db, user.id, major_name, CategoryType(major_type))
                    st.toast(f"Category '{major_name}' created!", icon="🏷️")
                    st.rerun()

    with col2:
        st.markdown("### New Sub-Category")
        majors = get_major_categories(db)
        if not majors:
            st.warning("Create a major category first.")
        else:
            major_map = {f"{c.name} ({c.type.value})": c.id for c in majors}
            
            with st.form("sub_cat_form"):
                parent_name = st.selectbox("Parent Category", list(major_map.keys()))
                sub_name = st.text_input("Name", placeholder="e.g. Electric Bill")
                
                if st.form_submit_button("Create Sub-Category", type="primary"):
                    if parent_name and sub_name:
                        parent_id = major_map[parent_name]
                        # Inherit type from parent
                        parent_obj = [c for c in majors if c.id == parent_id][0]
                        
                        create_category(db, user.id, sub_name, parent_obj.type, parent_id)
                        st.toast(f"Sub-Category '{sub_name}' created!", icon="🏷️")
                        st.rerun()

st.divider()
st.subheader("📚 Category List")

categories = get_categories(db)
if categories:
    # Display categories with delete option
    for cat in categories:
        parent_name = cat.parent.name if cat.parent else "None (Major)"
        level = "Sub-Category" if cat.parent else "Major"
        
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        
        with col1:
            st.markdown(f"**{cat.name}**")
        with col2:
            st.markdown(f"*{cat.type.value}*")
        with col3:
            st.markdown(f"{level}")
        with col4:
            st.markdown(f"{parent_name}")
        with col5:
            # Delete button with unique key
            if st.button("🗑️", key=f"delete_cat_{cat.id}", help="Delete category", type="secondary"):
                try:
                    delete_category(db, cat.id)
                    st.toast(f"Category '{cat.name}' deleted!", icon="🗑️")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
        
        st.markdown("---")
else:
    st.info("No categories defined yet.")


