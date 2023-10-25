import streamlit as st
from lib.quest.import_quests import import_quests
st.markdown("# Upload Quest Data")
st.sidebar.markdown("# Upload Quests")

uploaded_file = st.file_uploader("Choose import Excel file")

if uploaded_file is not None:
    run_import = st.button("Run Import")
    if run_import:
        upload_result = import_quests(uploaded_file)
        st.write(upload_result)

