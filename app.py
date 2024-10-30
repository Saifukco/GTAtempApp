import streamlit as st
import streamlit_dynamic_filters as DynamicFilters
from streamlit_dynamic_filters import DynamicFilters
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



@st.cache_data
def read_data(file):
    df = pd.read_excel(file)
    df['DATE']=pd.to_datetime(df['DATE']).dt.date
    return df

def main():
    st.title("GTA Dash Board")
    with st.spinner('Loading data...'):
        # Fetch data from MySQL database
        df = read_data('data.xlsx')
         # ---- SIDEBAR ----
    
    with st.sidebar:
        st.write("Select Date Range")

    with st.sidebar:
        start_date = st.date_input("Start Date", df['DATE'].min())
        end_date = st.date_input("End Date", df['DATE'].max())

    filtered_df_date = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
    dynamic_filters = DynamicFilters(filtered_df_date, filters=['Type of Outlet','City','Owner'])
    dynamic_filters.display_filters(location='sidebar')
    filtered_df = dynamic_filters.filter_df()
    # Assuming df is your DataFrame with 'LAT' and 'LONG' columns
    filtered_df['LAT'] = filtered_df['LAT'].astype(float)
    filtered_df['LONG'] = filtered_df['LONG'].astype(float)

    # Calculate the center of the map
    center_lat = np.mean(filtered_df['LAT'])
    center_lon = np.mean(filtered_df['LONG'])

    # Determine an appropriate zoom level
    lat_range = filtered_df['LAT'].max() - filtered_df['LAT'].min()
    lon_range = filtered_df['LONG'].max() - filtered_df['LONG'].min()
    zoom = 8  # Default zoom level

    if max(lat_range, lon_range) > 0:
        zoom = max(3, 10 - np.log(max(lat_range, lon_range)))

    # Create the scatter mapbox
    fig = px.scatter_mapbox(
        filtered_df, 
        lat="LAT", 
        lon="LONG", 
        hover_name="Name of the outlet", 
        hover_data=["State", "Owner"],
        color="Type of Outlet",  # Adding color based on the Type of Outlet
        color_discrete_sequence=px.colors.qualitative.Set1,  # Optional: Choose a color sequence
        zoom=zoom,  # Set the calculated zoom level
        center={"lat": center_lat, "lon": center_lon},  # Set the center of the map
        height=300
    )
    fig.update_traces(marker=dict(size=15))  # Adjust the size here
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    col1, col2, = st.columns(2)
    with col1:
        st.metric(label="Total Number Of Oultes", value=str(df['Submission Id'].count()))
    with col2:
        st.metric(label="Number Of Oultes", value=str(filtered_df['Submission Id'].count()))

    with st.container(border=True):
        st.plotly_chart(fig)



# Run the main function
if __name__ == '__main__':
    main()
