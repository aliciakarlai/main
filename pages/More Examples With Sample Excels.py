import streamlit as st
import requests
import pandas as pd
from io import BytesIO

st.title("More Examples")

#######################################
st.header("3 Interval Layers Colored by Status:")
status_interval="https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20Status_3%20Intervals.jpg"
st.image(status_interval, caption='3 Interval Layers Colored by Status')
st.write("Downloadable Examples:")

three_interval= "https://github.com/aliciakarlai/streamlit/raw/main/pages/3%20Intervals.xlsx"
# Fetch the file from GitHub
Interval_status = requests.get(three_interval)
Interval_status.raise_for_status()  # Check that the request was successful


# Create a download button for the Excel file
st.download_button(
    label="3 Interval Excel",
    data=Interval_status.content,
    file_name="3 Interval Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

status_url= "https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20Status.xlsx"
# Fetch the file from GitHub
status = requests.get(status_url)
status.raise_for_status()  # Check that the request was successful


# Create a download button for the Excel file
st.download_button(
    label="Well Status Excel",
    data= status.content,
    file_name="Well Status Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
#################################################################
### 5 INTERVAL image
st.header("5 Interval Layers Colored by Operator:")
operator_interval="https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20Operator_5%20Intervals.jpg"
st.image(operator_interval, caption='5 Interval Layers Colored by Operator')
st.write("Downloadable Examples:")

#5 interval well Excel
five_interval_url= "https://github.com/aliciakarlai/streamlit/raw/main/pages/5%20Intervals.xlsx"
five_interval= requests.get(five_interval_url)
five_interval.raise_for_status()  # Check that the request was successful


# Create a download button for the Excel file
st.download_button(
    label="5 Interval Well Excel",
    data= five_interval.content,
    file_name="five_interval Excel Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


##operator well Excel
operator_url= "https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20Operator.xlsx"
operator = requests.get(operator_url)
operator.raise_for_status()  # Check that the request was successful


# Create a download button for the Excel file
st.download_button(
    label="Operator Well Excel",
    data= operator.content,
    file_name="Operator Well Status Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


##############################################################################################

### vintage image
st.header("Colored By Vintage")
vintage_image_url="https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20Vintage_cropped.jpg"
st.image(vintage_image_url, caption='Colored By Vintage')
st.write("Downloadable Example:")

#5 interval well Excel
vintage_url= "https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20Vintage.xlsx"
vintage= requests.get(vintage_url)
vintage.raise_for_status()  # Check that the request was successful


# Create a download button for the Excel file
st.download_button(
    label="Vintage Well Excel",
    data= vintage.content,
    file_name="Vintage.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

##################################

### by API  image
st.header("Colored By API")
API_plot="https://github.com/aliciakarlai/streamlit/raw/main/pages/by%20API_cropped.jpg"
st.image(API_plot, caption='Colored By API')
st.write("Downloadable Example:")

#5 interval well Excel
API_url= "https://github.com/aliciakarlai/streamlit/raw/main/pages/By%20API.xlsx"
API= requests.get(API_url)
API.raise_for_status()  # Check that the request was successful


# Create a download button for the Excel file
st.download_button(
    label="API Well Excel",
    data= API.content,
    file_name="API.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

