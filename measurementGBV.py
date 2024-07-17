import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_pdf import PdfPages
from io import StringIO
from io import BytesIO
import io
import plotly.express as px

st.title("Simple GBV With Background Colors")
st.header("Select The Data")
# Get the file
well_file = st.file_uploader("Choose a file with the well data (Excel workbook)", type=["xlsx", "xls"])
unique_apis=[]
if well_file is not None:
    # To read file as bytes:
    bytes_data = well_file.getvalue()
    
    # To convert to a bytes based IO:
    bytesio = BytesIO(bytes_data)
    
    # To read the Excel file:
    df = pd.read_excel(bytesio)
    result_well= st.button("Check Well Data")

    if result_well:
        try:
            df = df[['API_UWI', 'NNSAPI_UWI', '2dDistanceMean_FT', 'VerticalDistanceMean_FT', 'NNSSideHeel','NNSSideToe', 'WBT_ENVInterval','ColorCode']]
            st.write("Good to go!")
            unique_apis = df['API_UWI'].unique()
            st.write(unique_apis)
        except:
            st.write("Well Data does not have all necessary columns: API_UWI, NNSAPI_UWI, 2dDistanceMean_FT, VerticalDistanceMean_FT, NNSSideHeel,NNSSideToe, WBT_ENVInterval,ColorCode")


selected_api = st.text_input("Selected API:")
st.write("This is you (0,0) point all other wells are based off of.")


#heel or toe?
st.header("Play With The Details")
direction_options=['Heel','Toe']
direction_selected=st.selectbox("How would you like to format direction?",options=direction_options)

measurement_options=['Standard(7.08 x 5)','Custom']
measurement_selected=st.selectbox("How would you like to format size? (inches)",options=measurement_options)

#for the measurements
if measurement_selected == "Custom":
    custom_height=st.number_input("height?", min_value=0.000000, step=0.000001, max_value=20.00001, value=0.000001, format="%f")
    plotting_area_height_in = custom_height
    
    custom_width=st.number_input("width?", min_value=0.000000, step=0.000001, max_value=20.00001, value=0.000001, format="%f")
    plotting_area_width_in = custom_width
else:
    plotting_area_width_in = 7.08661
    plotting_area_height_in = 5
    
run_button= st.button("Run") 


if run_button:

    #for the heel toe:
    if direction_selected =="Toe":
        df['2dDistanceMean_FT'] = df.apply(lambda row: -row['2dDistanceMean_FT'] if row['NNSSideToe'] == 'LEFT' else row['2dDistanceMean_FT'], axis=1)
    else:
        df['2dDistanceMean_FT'] = df.apply(lambda row: -row['2dDistanceMean_FT'] if row['NNSSideHeel'] == 'LEFT' else row['2dDistanceMean_FT'], axis=1)

    # Modify the X values based on the NNSSideHeel condition
    df['VerticalDistanceMean_FT']=df['VerticalDistanceMean_FT']*-1
    
    # Display unique API_UWI values
    unique_apis = df['API_UWI'].unique()


    #create a new df of the first set of connnections
    df_og=df[(df['API_UWI']==selected_api)]
    df_1=df_og[['NNSAPI_UWI','2dDistanceMean_FT','VerticalDistanceMean_FT']]

    #add selected API as (0,0) to the top of row
    new_row=pd.DataFrame([{'NNSAPI_UWI': selected_api, '2dDistanceMean_FT': 0, 'VerticalDistanceMean_FT': 0, }])
    df_1 = pd.concat([new_row, df_1]).reset_index(drop = True)
    df_1 = df_1.rename(columns={'NNSAPI_UWI': 'API_UWI','2dDistanceMean_FT': 'X','VerticalDistanceMean_FT': 'Y'})


    #index match from df1 for new X and Y
    df=df.merge(df_1[['API_UWI','X']], how='left', on='API_UWI')
    df=df.merge(df_1[['API_UWI','Y']], how='left', on='API_UWI')
    df['Final X']= df['X']+df['2dDistanceMean_FT']
    df['Final Y']= df['Y']+df['VerticalDistanceMean_FT']


    #add remaining API's to df_1
    visited_api = set(df_1['API_UWI'])
    unique_apis = df['API_UWI'].unique()
    remaining_apis = list(set(unique_apis) - visited_api)  # Convert remaining APIs to list
    df_1 = df_1.rename(columns={'API_UWI':'NNSAPI_UWI','X':'Final X','Y':'Final Y'})

    #create new df with averages for remaining API's
    df_2=pd.DataFrame({'NNSAPI_UWI':remaining_apis})

    # Calculate mean Final X and Final Y for each remaining NNSAPI_UWI
    means = df.groupby('NNSAPI_UWI')[['Final X', 'Final Y']].mean().reset_index()
    df_2 = df_2.merge(means, how='left', left_on='NNSAPI_UWI', right_on='NNSAPI_UWI')
    # Use pd.concat to append df_2 to df_1
    df_appended = pd.concat([df_1, df_2], ignore_index=True)
    df_appended = df_appended.rename(columns={'NNSAPI_UWI':'API_UWI'})

    #make the colors
    unique_colors= df[['API_UWI','ColorCode']].drop_duplicates()
    unique_intervals= df[['API_UWI','WBT_ENVInterval']].drop_duplicates()
    df_appended=df_appended.merge(unique_colors[['API_UWI','ColorCode']], how='left', on='API_UWI')
    df_appended=df_appended.merge(unique_intervals[['API_UWI','WBT_ENVInterval']], how='left', on='API_UWI')
    df_appended=df_appended[df_appended['API_UWI'].isin(unique_apis)]
    df_appended['ColorCode']=df_appended['ColorCode'].fillna('#58575a')
    fig=px.scatter(df_appended,x= "Final X", y="Final Y", color="ColorCode",hover_data=['API_UWI','WBT_ENVInterval'])



    # Remove the gridlines
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    # Increase the size of the points
    fig.update_traces(marker=dict(size=20))

    # Show the sample
    event = st.plotly_chart(fig, key="iris", on_select="rerun")
    event.selection


    # Extract coordinates
    df_sorted = df_appended.sort_values(by='Final X')
    sorted_coords = df_sorted[['Final X', 'Final Y']].values

    ###make the area
    # Define sizes in inches
    total_fig_width_in = 8.5
    total_fig_height_in = 11
    plotting_area_width_in = 7.08661
    plotting_area_height_in = 5

    # Create the figure and axis
    matplotlib_fig, ax = plt.subplots(figsize=(total_fig_width_in, total_fig_height_in))

    # Calculate margins and set the plotting area
    left_margin = (total_fig_width_in - plotting_area_width_in) / (2 * total_fig_width_in)
    bottom_margin = (total_fig_height_in - plotting_area_height_in) / (2 * total_fig_height_in)
    ax_width_fraction = plotting_area_width_in / total_fig_width_in
    ax_height_fraction = plotting_area_height_in / total_fig_height_in
    ax.set_position([left_margin, bottom_margin, ax_width_fraction, ax_height_fraction])

    #plot the points

    neutron_gray = '#807f83'
    none='#58575a'
    pointsize=11.34*11.34
    font_size_graphics = 7

    plt.scatter(df_sorted['Final X'], df_sorted['Final Y'],c=df_sorted['ColorCode'], zorder=2, edgecolors=neutron_gray, linewidths=1, s=pointsize)

    # Add dashed lines and labels
    for i in range(1, len(sorted_coords)):
        x0, y0 = sorted_coords[i - 1]
        x1, y1 = sorted_coords[i]
        plt.plot([x0, x1], [y0, y0], 'k--', linewidth=1, zorder=1)  # Horizontal dashed line
        plt.plot([x1, x1], [y0, y1], 'k--', linewidth=1, zorder=1)  # Vertical dashed line
        
        x_diff = abs(x1 - x0)
        y_diff = abs(y1 - y0)
        
        plt.text((x0 + x1) / 2, y0, f' {int(x_diff):,}\'', ha='center', va='bottom', color='black', fontsize=font_size_graphics, fontweight='bold')
        plt.text(x1, (y0 + y1) / 2, f' {int(y_diff):,}\'', ha='left', va='center', color='black', fontsize=font_size_graphics, fontweight='bold')

    plt.grid(False)

    for spine in ax.spines.values():
        spine.set_edgecolor(neutron_gray)
        spine.set_linewidth(.75)

    # Save the plot as a PDF file
    pdf_buffer = io.BytesIO()
    plt.savefig(pdf_buffer, format='pdf')
    pdf_buffer.seek(0)

    # Add a download button for the PDF file
    st.download_button(
        label="Download plot as PDF",
        data=pdf_buffer,
        file_name='scatter_plot.pdf',
        mime='application/pdf'
)    
