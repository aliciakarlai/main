import streamlit as st
import requests

st.title("Trouble Shooting:wrench:")

st.subheader("Well API Points Aren't Coloring The Way I want It To")

st.markdown(
"""
This error occurs because the color is likely attached to the wrong column. To fix this, try the following steps:
- Open the Well Data Excel and ensure that ColorCode is index matched to API_UWI, not NNSAPI_UWI.
- Check that all values in the ColorCode column are valid hex color codes and include the #.
- If the well point is grey, there is not a valid color code for that API.
"""
)

st.subheader("Not All of the API's I Want Are Showing On The Chart")

st.markdown(
"""
This occurs because the API does not appear on the API_UWI list. To fix this, try the following steps:
- Open the Well Data Excel and ensure that all desired APIs are in the columns.
- If the API is in the NNSAPI_UWI column but not in the API_UWI column, it will not show.
- The GBV generator only looks up to 2 connections of the selected API. Check the how it works page to learn more. Try a smaller list to see all API's. 
"""
)

st.subheader("Not All of the Intervals I Want Are Showing")


st.markdown(
"""
To fix this, try the following steps:
- Open the Interval Excel and ensure that the WBT_ENVInterval column has no repeating values.
- Check that the Color column has no repeating colors, and all values are valid hex colors and include the #.
"""
)

st.header("Error Messages")


st.subheader("Type Error")
#get image url
Error_1="https://github.com/aliciakarlai/streamlit/raw/main/pages/error_1.jpg"

# Display the image
st.image(Error_1)

st.markdown(
"""
This error occurs because the WBT_ENVInterval tabs on the Interval Excel and the Well Excel do not match. To fix this, try the following steps:
- Open both Excel workbooks and ensure they contain the correct data you want to work with.
- Verify that the data in the WBT_ENVInterval tab in the Interval Excel is spelled correctly and matches how it is spelled in Prism.
- Ensure that the data in the Color column has a hex color for each interval, and make sure each interval has a different color.

"""
)

st.subheader("Value Error")

Error_3="https://github.com/aliciakarlai/streamlit/raw/main/pages/error%203.jpg"

st.image(Error_3)

st.markdown(
"""
This could occur for a number of reasons. To fix this, try the following steps:
- You did not select a valid API; try pasting an API from the list.
- There are not enough connections in the 4D spacing table. Open Prism and create a Gun Barrel View, and insert no more APIs than the amount shown in the GBV. 
"""
)
