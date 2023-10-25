import streamlit as st


from lib.user.create_user import create_user


st.markdown("# Create User")
st.sidebar.markdown("# Create User")

with st.form("create_user", clear_on_submit=True):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password")
    group_id = st.text_input("Group ID")
    is_group_leader = st.checkbox("Is Group Leader")

    submitted = st.form_submit_button("Create User")

if submitted:
    create_user(first_name + " " + last_name, email, password, group_id, is_group_leader)


