import streamlit as st
import pandas as pd
from database import get_db
from models import CategoryType
from crud import create_category, get_categories, get_major_categories
from styles import get_custom_css

st.set_page_config(page_title="Manage Categories", page_icon="🏷️")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.header("🏷️ Manage Categories")
st.markdown("Organize your finances with custom categories.")

db = next(get_db())

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### New Major Category")
        with st.form("major_cat_form"):
            major_name = st.text_input("Name", placeholder="e.g. Utilities, Salary")
            major_type = st.selectbox("Type", ["Income", "Expense"])
            
            if st.form_submit_button("Create Major", type="primary"):
                if major_name:
                    create_category(db, major_name, CategoryType(major_type))
                    st.success(f"Category '{major_name}' created!")
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
                        
                        create_category(db, sub_name, parent_obj.type, parent_id)
                        st.success(f"Sub-Category '{sub_name}' created!")
                        st.rerun()

st.divider()
st.subheader("📚 Category List")

categories = get_categories(db)
if categories:
    # Flatten for display
    data = []
    for cat in categories:
        parent_name = cat.parent.name if cat.parent else "None (Major)"
        data.append({
            "Name": cat.name,
            "Type": cat.type.value,
            "Level": "Sub-Category" if cat.parent else "Major",
            "Parent": parent_name
        })
    df = pd.DataFrame(data).sort_values(by=["Type", "Level", "Name"])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No categories defined yet.")

