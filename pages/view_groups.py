import streamlit as st
from lib.church.get_groups import get_groups
import pandas as pd

st.markdown("# View Groups")
st.sidebar.markdown("# View Groups")
groups = get_groups()
df = pd.DataFrame(groups)
st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

