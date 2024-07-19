import streamlit as st

st.title("How it Works:gear:")


st.header("GBV With Background Colors:rainbow:")
colored_image_url="https://github.com/aliciakarlai/streamlit/raw/main/pages/color_connections.jpg"


# Display the image
st.image(colored_image_url)

st.markdown(
"""
- After inputting the Excel workbook, it calculates the center point on the X-axis. If there is an even number of well points, it takes the two center points and picks the right one. That is the pink point.
- It takes point 1 (center API) and finds all of its nearest neighbors. Those are the purple points.
- Then it takes the nearest neighbors' points and plots all of the points connected to those nearest neighbors. Those are the green points.
- If an API is in the NNAPI column but not in the API column, it will not show on the chart.
- It then uses the second Excel sheet with all of the intervals and performs the equivalent of an index match to match each well point to the interval in the interval list.
- It vertically normalizes by plotting the well in the middle of the interval.
- Finally, it adds labels to each interval based on the X min.
"""
)


st.link_button("Check Out The GBV Code", "https://github.com/aliciakarlai/streamlit/blob/main/pages/GBV%20With%20Background%20Colors.py")



st.header("GBV With Measurements:straight_ruler:")

# URL of the image on GitHub
image_url = "https://github.com/aliciakarlai/streamlit/raw/main/pages/Connections_measured.jpg"
st.image(image_url)
st.markdown(
"""
- After inputting the Excel and selecting the API, it takes the selected API and plots it first at point (0,0). That's the pink point.
- It takes point 1 (center API) and finds all of its nearest neighbors. Those are the green points.
- Then it takes the nearest neighbors' points and plots all of the points connected to those nearest neighbors. Those are the purple points.
- It then calculates the order from left to right and calculates the distance between each point vertically and horizontally, and plots it down.
- If an API is not in the API_UWI column but in the NNSAPI column, it will not show on the chart.
"""
)


st.link_button("Check Out The Code", "https://github.com/aliciakarlai/streamlit/blob/main/pages/GBV%20With%20Measurements.py")
