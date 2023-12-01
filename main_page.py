from google.oauth2 import service_account
import streamlit as st
import firebase_admin
import json
from google.cloud import firestore
from firebase_admin import credentials

if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["textkey"], strict=False)
    cred = firebase_admin.credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

st.markdown("# Salt & Light Admin")
st.sidebar.markdown("# Salt & Light Admin")
