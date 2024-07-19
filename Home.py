import streamlit as st

st.title("Gun Barrel View Generator")
st.write("Create 2 different types of GBV's in minutes")

st.header("GBV With Background Colors:rainbow:")

#get image url
Measured_url="https://github.com/aliciakarlai/streamlit/raw/main/GBVcolors.jpg"

# Display the image
st.image(Measured_url, width=550)

#get image url
st.header("GBV With Measurements:straight_ruler:")

# Display the image
Color_url="https://github.com/aliciakarlai/streamlit/raw/main/GBVmeasured_01.jpg"
st.image(Color_url, width=550)
