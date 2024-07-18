import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_pdf import PdfPages
from io import StringIO
from io import BytesIO
import io
import plotly.express as px

st.title("GBV With Background Colors:rainbow:")

# Get the file
well_file = st.file_uploader("Choose a file with the well data (Excel workbook)", type=["xlsx", "xls"])

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
        st.write("Good to go!:clap:")
    except:
        st.write("Error :poop: Well Data does not have all necessary columns: API_UWI, NNSAPI_UWI, 2dDistanceMean_FT, VerticalDistanceMean_FT, NNSSideHeel,NNSSideToe, WBT_ENVInterval,ColorCode")


###############get the interval data
# Get the file

interval_file = st.file_uploader("Choose a file with the interval data (Excel workbook)", type=["xlsx", "xls"])

if interval_file is not None:
    # To read file as bytes:
    bytes_I_data = interval_file.getvalue()
    
    # To convert to a bytes based IO:
    bytesi_I = BytesIO(bytes_I_data)
    
    # To read the Excel file:
    df_Interval = pd.read_excel(bytesi_I)

result_interval= st.button("Check Interval Data") 
if result_interval:
    try:
        df_interval = df_Interval[['WBT_ENVInterval','Interval','Color']]
        st.write("Good to go!:clap:")
    except:
        st.write("Error :poop: Well Data does not have all necessary columns: WBT_ENVInterval,Interval,Color")  
        
#heel or toe?
st.header("Play With The Details")
direction_options=['Heel','Toe']
direction_selected=st.selectbox("How would you like to format direction?",options=direction_options)


measurement_options = ['Standard(7.08 x 5)', 'Custom']
measurement_selected = st.selectbox("How would you like to format size? (inches)", options=measurement_options)

# For the measurements
if measurement_selected == "Custom":
    custom_height = st.number_input("Height?", min_value=0.000000, step=0.000001, max_value=8.01201, value=0.000001, format="%f")
    plotting_area_height_in = custom_height
    
    custom_width = st.number_input("Width?", min_value=0.000000, step=0.000001, max_value=7.08611, value=0.000001, format="%f")
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

    # Find the unique API_UWI values and sort them by the mean horizontal distance
    unique_api_uwi = df.groupby('API_UWI')['2dDistanceMean_FT'].mean().sort_values().index.tolist()

    # Determine the center API_UWI
    n = len(unique_api_uwi)
    if n % 2 == 1:
        center_api_uwi = unique_api_uwi[n // 2]
    else:
        center_api_uwi = unique_api_uwi[n // 2 - 1]


    selected_api= center_api_uwi

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


    #add colors and intervals
    unique_colors= df[['API_UWI','ColorCode']].drop_duplicates()
    unique_intervals= df[['API_UWI','WBT_ENVInterval']].drop_duplicates()
    df_appended=df_appended.merge(unique_colors[['API_UWI','ColorCode']], how='left', on='API_UWI')
    df_appended=df_appended.merge(unique_intervals[['API_UWI','WBT_ENVInterval']], how='left', on='API_UWI')
    df_appended=df_appended[df_appended['API_UWI'].isin(unique_apis)]
    df_appended['ColorCode']=df_appended['ColorCode'].fillna('#58575a')
    # Ensure df_Interval is a DataFrame


    # Count different types of variables in the specified column
    def count_interval_types(df, column_name):
        type_counts = df[column_name].apply(lambda x: type(x).__name__).value_counts()
        return type_counts

    column_name = 'WBT_ENVInterval'
    type_counts = count_interval_types(df_Interval, column_name)

    # Map intervals to their corresponding y-ranges
    interval_list = df_Interval['WBT_ENVInterval'].unique()
    interval_ranges = {layer: (1 - (i + 1) / len(interval_list), 1 - i / len(interval_list)) for i, layer in enumerate(interval_list)}

    # Assign y-ranges to df_appended
    df_appended['IntervalRange'] = df_appended['WBT_ENVInterval'].map(interval_ranges)

    # Extract x and y from IntervalRange and calculate the midpoint
    #df_appended['IntervalRange'] = df_appended['IntervalRange'].apply(lambda x: eval(x))
    df_appended['Interval Y'] = df_appended['IntervalRange'].apply(lambda x: (x[0] + x[1]) / 2)


    layers = df_Interval['WBT_ENVInterval']
    intervals_with_points = set(df_appended['WBT_ENVInterval'])
    
    ####make the fig that shows up on the browser
    fig=px.scatter(df_appended,x= "Final X", y="Interval Y", color="ColorCode",hover_data=['API_UWI','WBT_ENVInterval'])
    event = st.plotly_chart(fig, key="iris", on_select="rerun")
    event.selection
    
    #st.write(df_appended)
    layers = df_Interval['WBT_ENVInterval']
    intervals_with_points = set(df_appended['WBT_ENVInterval'])

    # For the pdf format
    total_fig_width_in = 8.5
    total_fig_height_in = 11
    # Create a figure and axis with specified size
    fig, ax = plt.subplots(figsize=(total_fig_width_in, total_fig_height_in))

    # Calculate the margins of the graph
    left_margin = (total_fig_width_in - plotting_area_width_in) / (2 * total_fig_width_in)
    bottom_margin = (total_fig_height_in - plotting_area_height_in) / (2 * total_fig_height_in)
    ax_width_fraction = plotting_area_width_in / total_fig_width_in
    ax_height_fraction = plotting_area_height_in / total_fig_height_in
    ax.set_position([left_margin, bottom_margin, ax_width_fraction, ax_height_fraction])

    neutron_gray = '#807f83'
    none = '#58575a'
    pointsize = 11.34 * 11.34
    font_size_graphics = 7

    #create a dictionary of colors
    interval_colors = df_Interval.set_index('WBT_ENVInterval')['Color'].to_dict()

    # Plot horizontal layers in the background
    for i, layer in enumerate(layers):
        if layer in interval_ranges:  # Ensure the layer is in interval_ranges
            ymin, ymax = interval_ranges[layer]
            color = interval_colors.get(layer,'C0')
            alpha = 0.4 if layer in intervals_with_points else 0.2
            ax.axhspan(ymin=ymin, ymax=ymax, color=color, alpha=alpha, linewidth=0)


    #figute out the x max and min for the plotting area and where to place the labels
    x_min =df_appended['Final X'].min()
    x_max = df_appended['Final X'].max()
    x_max_limit=x_max *1.05
    x_min_limit=x_min *1.05

    # Create a dictionary to map WBT_ENVInterval to Interval for labeling
    interval_labels = df_Interval.set_index('WBT_ENVInterval')['Interval'].to_dict()

    for i, label in enumerate(layers):
        if label in interval_ranges:  # Ensure the label is in interval_ranges
            ymin, ymax = interval_ranges[label]
            ax.text(x_min-5, ymax - 0.01, interval_labels[label], va='top', ha='left', fontsize=font_size_graphics, fontweight='bold', bbox=dict(facecolor='none', alpha=0.5, edgecolor='none', pad=5))

    #plot the points
    for _, row in df_appended.iterrows():
        plt.scatter(row['Final X'], row['Interval Y'], color=row['ColorCode'], label=row['WBT_ENVInterval'], edgecolors=neutron_gray, linewidths=1, s=pointsize)


    #edit the max and min of the plotting area
    #ax.set_xlim(x_min_limit, x_max_limit)
    ax.set_ylim(0, 1)

    #remove the tics
    plt.tick_params(left = False, right = False , labelleft = False , 
                    labelbottom = False, bottom = False) 

    #edit the colors and thickness of the edges
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

    
    
