import streamlit as st
from lib.church.create_church import create_church_in_database

st.markdown("# Create Church")
st.sidebar.markdown("# Create Church")

with st.form("church_information", clear_on_submit=True):
    title = st.text_input('Church Name')
    website = st.text_input("Website")
    address = st.text_input("Address")
    bio = st.text_area("Bio")
    contact = st.text_input("Contact")

    submitted = st.form_submit_button("Add Church")

if submitted:
    create_church_in_database(title, website, address, bio, contact)
