import streamlit as st
import streamlit_dynamic_filters as DynamicFilters
from streamlit_dynamic_filters import DynamicFilters
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



@st.cache_data
def read_data(file):
    df = pd.read_excel(file)
    df['DATE']=pd.to_datetime(df['DATE']).dt.date
    return df

def main():
    st.title("GTA Daash Board")
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
    dynamic_filters = DynamicFilters(filtered_df_date, filters=['Type of Outlet','City.1','Owner'])
    dynamic_filters.display_filters(location='sidebar')
    filtered_df = dynamic_filters.filter_df()
    filtered_df['LAT'] = filtered_df['LAT'].astype(float)
    filtered_df['LONG'] = filtered_df['LONG'].astype(float)

    fig = px.scatter_mapbox(
        filtered_df, 
        lat="LAT", 
        lon="LONG", 
        hover_name="Name of the outlet", 
        hover_data=["State", "Owner"],
        color="Type of Outlet",  # Adding color based on the Type of Outlet
        color_discrete_sequence=px.colors.qualitative.Set1,  # Optional: Choose a color sequence
        zoom=5, 
        height=600,  # Adjust the height of the map
        width=3000   # Adjust the width of the map
    )
    # Increase the size of the dots
    fig.update_traces(marker=dict(size=10)) 
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