import streamlit as st
import pandas as pd
from io import BytesIO
import requests

    
st.title("Instructions:book:")
st.header("GBV With Measurements:straight_ruler:")

st.markdown(
 """
Download the 4D spacing table:
- In Prism filter for the list of API's wanted. If it just in the NNSAPI and not the API column it will not show up or it will be colored incorrectly. 
- The table needs to have the columns API_UWI, NNSAPI_UWI, 2dDistanceMean_FT, VerticalDistanceMean_FT, NNSSideHeel, NNSSideToe, WBT_ENVInterval, NNS_ENVInterval. Even if you are not using all of the columns you need to be present. 
- Columns in prism are called WBT API / UWI, Nearest Neighbour API / UWI, 2D Distance, Mean (ft), Vertical Distance, Mean (ft), Nearest Neighbour Side at Heel, Nearest Neighbour Side at Toe, ENV Interval WBT, ENV Interval NNS.
- If any of the columns are miss labeled the code will not run. 

Edit the Excel:
- Insert a column named ColorCode. The code will not run without this exact label. Each row in this column must have a color code, format as a Hex code, to determine the color of the point on the graph. 
- Color is asigned by API.
- Close the Excel, the code cannot run if the excel is open. It needs to be saved as a workbook, not a CSV. 

Upload the Excel File:
- Use the drag and drop feature to upload the Excel file.
- Click the "Check Well Data" button to verify if it is a valid file. This will also output a list of all unique APIs in the file.
- Copy one API from the list and paste it into the select API box. This API will be the point (0,0) on the chart, with all other points plotted based on their connection to this point, similar to selecting a well in Prism.

Adjust the Details:
- Choose whether the direction is based on heel or toe.
- Edit the size of the chart, either using the standard size or customizing it. The maximum width is 7.08611 and the maximum height is 8.01201.

Run the Code:
- This will generate an interactive graph showing the layout of the points. You can hover over the points to see the interval or API.
- Note that connections are not shown in this view, but they will be included once you download the graph.

Download:
- If you are satisfied with the graph, click "Download" to save a graphics-ready PDF.
"""
)

st.write("Downloadable Examples:")

# URL of the Excel file on GitHub
well_measure_url = "https://github.com/aliciakarlai/streamlit/raw/main/pages/well_measure.xlsx"

# Fetch the file from GitHub
response_measure_well = requests.get(well_measure_url)
response_measure_well.raise_for_status()  # Check that the request was successful

# Create a download button for the Excel file
st.download_button(
    label="GBV Well Excel",
    data=response_measure_well.content,
    file_name="Well Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

#create link button for colors
st.link_button("Custom Colors", "https://gbvgenerator.streamlit.app/~/+/Instructions#example-colors")


# Add a header to your Streamlit app

st.header("GBV With Background Colors:rainbow:")

st.markdown(
 """
Download the 4D Spacing Table:
- Use Prism to get the list of desired APIs. If the API is only in the NNSAPI column and not in the API column, it will not appear or it will be colored incorrectly.
- The table must include the following columns: API_UWI, NNSAPI_UWI, 2dDistanceMean_FT, VerticalDistanceMean_FT, NNSSideHeel, NNSSideToe, WBT_ENVInterval, NNS_ENVInterval. All columns must be present even if they are not used.
- Columns in prism are called WBT API / UWI, Nearest Neighbour API / UWI, 2D Distance, Mean (ft), Vertical Distance, Mean (ft), Nearest Neighbour Side at Heel, Nearest Neighbour Side at Toe, ENV Interval WBT, ENV Interval NNS.
- If any of the columns are miss labeled the code will not run. 
 
Edit the Excel File:
- Insert a column named ColorCode. The code will not run without this exact label. Each row in this column must have a color code, formatted as a Hex code, to determine the color of the point on the graph.
- Color is asigned by API.
- Close the Excel file before running the code. Save it as a workbook, not as a CSV.

Create Interval Excel:
- Create a second Excel workbook with the columns WBT_ENVInterval, Interval, Color.
- The first column, WBT_ENVInterval, will be the intervals that match the output in Prism and will perform an index match with the Well Data Excel. The Interval column will be what you want the interval label to be when exported to a PDF.
- Finally, the Color column will be the color of the interval, formatted as a Hex code.
-There can NOT be any blank rows.
- You can insert rows for intervals that do not have well points but want to be displayed.
- The intervals are displayed top down (row 2 will be the first interval).

Upload Excels to App:
- Insert the Well Excel into the first file drag and drop. Click the "Check Well Data" button to see if it meets the Excel requirements.
- Insert the Interval Excel into the second file drag and drop. Click the "Check Interval Data" button to see if it meets the Excel requirements.

Adjust the Details:
- Choose whether the direction is based on heel or toe.
- Edit the size of the chart, either using the standard size or customizing it. The maximum width is 7.08611 and the maximum height is 8.01201.

Run the Code:
- This will generate an interactive graph showing the layout of the points. You can hover over the points to see the interval or API.
- Note that intervals are not shown in this view, but they will be included once you download the graph.

Download:
- If you are satisfied with the graph, click "Download" to save a graphics-ready PDF.
"""
)

st.write("Downloadable Examples:")
# URL of the Excel file on GitHub
well_url = "https://github.com/aliciakarlai/streamlit/raw/main/pages/Well%20Data.xlsx"

# Fetch the file from GitHub
response_well = requests.get(well_url)
response_well.raise_for_status()  # Check that the request was successful

# Create a download button for the Excel file
st.download_button(
    label="Well Excel",
    data=response_well.content,
    file_name="Well Data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# URL of the Excel file on GitHub
interval_url = "https://github.com/aliciakarlai/streamlit/raw/main/pages/Interval%20Data.xlsx"

# Fetch the file from GitHub
response_interval = requests.get(interval_url)
response_interval.raise_for_status()  # Check that the request was successful

# Create a download button for the Excel file
st.download_button(
    label="Interval Excel",
    data=response_interval.content,
    file_name="Well Interval.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Add a header
st.header("Example Colors")

# URL of the image on GitHub
image_url = "https://github.com/aliciakarlai/streamlit/raw/main/pages/Example%20Colors.png"

# Display the image
st.image(image_url)


