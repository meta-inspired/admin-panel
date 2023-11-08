import streamlit as st
from lib.church.create_group import create_group
from lib.church.get_churches import get_churches

st.markdown("# Create Group")
st.sidebar.markdown("# Create Group")

with st.form("group_information", clear_on_submit=True):
    churches = get_churches()
    church_names = []
    for church in churches:
        church_names.append(church["title"])
    church_selection = st.selectbox("Choose church for group", church_names)
    name = st.text_input("Name")
    bio = st.text_area("Bio")
    image = st.text_input("Image URL")
    is_private = st.checkbox("Is group private")
    journey_id = st.text_input("Journey ID")
    meeting_link = st.text_input("Meeting Link")
    group_code = st.text_input("Group Code")

    submitted = st.form_submit_button("Create Group")

if submitted:
    church_id = -1
    for church in churches:
        if church_selection == church["title"]:
            church_id = church["id"]
    create_group(name, bio, image, is_private, journey_id, meeting_link, church_id, group_code)

