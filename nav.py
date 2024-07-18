import streamlit as st

pages = st.navigation([
    st.Page("home.py", title="Home"),
    st.Page("SimpleGBV.py", title="GBV with Background Colors"),
    st.Page("measurementGBV.py", title="GBV With Measurements"),
    st.Page("Instructions.py", title="Instructions"),  
])

pg = st.navigation(pages)
pg.run()
