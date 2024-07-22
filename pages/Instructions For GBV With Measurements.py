import streamlit as st
import pandas as pd
from io import BytesIO
import requests

    
st.title("Instructions:book:")
st.header("GBV With Measurements:straight_ruler:")

st.markdown(
 """
Decide What Gun Barrel to Make:
- Open prism and load the gun barrel you would like to make. 
- In Prism filter for the list of API's that show up in the GBV.
- If there are not enough connections it will not plot.

Download the 4D spacing table:
- In Prism filter for the list of API's wanted. If it just in the NNSAPI (nearest neighbour API) and not the API column it will not show up or it will be colored incorrectly. 
- The table needs to have the columns API_UWI, NNSAPI_UWI, 2dDistanceMean_FT, VerticalDistanceMean_FT, NNSSideHeel, NNSSideToe, WBT_ENVInterval, NNS_ENVInterval. Even if you are not using all of the columns you need to be present. 
- Columns in prism are called WBT API / UWI, Nearest Neighbour API / UWI, 2D Distance, Mean (ft), Vertical Distance, Mean (ft), Nearest Neighbour Side at Heel, Nearest Neighbour Side at Toe, ENV Interval WBT, ENV Interval NNS.


Edit the Excel:
- Insert a column named ColorCode, if this is mislabeled it will not run. The code will not run without this exact label. Each row in this column must have a color code, format as a Hex code (ex.#EF509A) , to determine the color of the point on the graph. 
- Color is assigned by API. You can choose to color by interval, vintage year, unique API or whatever you want. Just make sure all rows with that API and there NN conection have the same color code. 
- Close the Excel, the code cannot run if the excel is open. It needs to be saved as a WORKBOOK (.xlsx), not a CSV. 

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


# Add a header
st.header("Example Colors")
colors_url="https://github.com/aliciakarlai/streamlit/raw/main/pages/All%20COLORS.xlsx"
# Read the Excel file into a DataFrame
df = pd.read_excel(colors_url)

# Display the DataFrame in Streamlit
st.dataframe(df)

# URL of the image on GitHub
image_url = "https://github.com/aliciakarlai/streamlit/raw/main/pages/Example%20Colors.png"

# Display the image
st.image(image_url)
