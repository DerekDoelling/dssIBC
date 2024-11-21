import streamlit as st
import numpy as np
import pandas as pd
import openpyxl

# Set page title and layout
st.set_page_config(page_title='IBC Data Explorer Dashboard', page_icon='📊', layout='wide')

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Import", "Preset Graphs", "Custom Graph", "Feedback"])

# Page routing
if page == "Import":
    import page.folder as folder
    folder.app()
elif page == "Preset Graphs":
    import page.preset as preset
    preset.app()
elif page == "Custom Graph":
    import page.custom as custom
    custom.app()
elif page == "Feedback":
    import page.feedback as feedback
    feedback.app()