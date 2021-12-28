import warnings

import streamlit as st
import pandas as pd
from datetime import datetime

# Local imports
from functions import df_preparation, get_transformed_params,  get_estimation, bar_chart_types, bar_chart_state_city

warnings.filterwarnings("ignore")

# Path for streamlit
path_1 = 'Project_10_House_prices_app/'
# Path for local host (current folder)
path_2 = ''

try:
    df, states, types, heatings, states_cities, cities_zip = df_preparation(path_1)
    path = path_1

except:
    df, states, types, heatings, states_cities, cities_zip = df_preparation(path_2)
    path = path_2


def app_body():

    # Selection part
    st.sidebar.write('Mandatory fields: ')
    property_type = st.sidebar.selectbox(label='Select property type:', options=types)
    state = st.sidebar.selectbox(label='Select state:', index=28, options=states)
    city = st.sidebar.selectbox(label='Select city:', index=0, options=["No city/other"] + states_cities[state])
    if city == 'No city/other':
        zip = st.sidebar.selectbox(label='Select zip:', index=0, options=["No zip/other"])
        sqft = st.sidebar.text_input(label='Enter total lot/house area, sqft', value=1100)
    else:
        zip = st.sidebar.selectbox(label='Select zip:', options=["No zip/other"] + cities_zip[city])
        sqft = st.sidebar.text_input(label='Enter total lot/house area, sqft', value=1100)

    more_params = st.sidebar.checkbox('I have additional parameters to enter (increases price accuracy)', value=False)

    if more_params:
        left_column_00, right_column_00, left_column_01 = st.columns(3)
        if property_type == 'LAND':
            beds = left_column_00.number_input(label='# of bedrooms:', min_value=0.0, max_value=0.0, value=0.0)
            baths = left_column_00.number_input(label='# of bathrooms:', min_value=0.0, max_value=0.0, value=0.0)
        else:
            beds = left_column_00.number_input(label='# of bedrooms:', min_value=0.0, max_value=15.0, step=0.5, value=3.0)
            baths = left_column_00.number_input(label='# of bathrooms:', min_value=0.0, max_value=15.0, step=0.5, value=2.0)

        pool = right_column_00.selectbox(label='Private pool:', index=0, options=['No info', 'Yes', 'No'])
        fireplace = right_column_00.selectbox(label='Fireplace:', index=0, options=['No info', 'Yes', 'No'])
        parking = left_column_01.selectbox(label='Parking:', index=0, options=['No info', 'Yes', 'No'])
        heating = left_column_01.selectbox(label='Heating type:', index=0, options=["No info"] + heatings)
    else:
        if property_type == 'LAND':
            beds = 0.0
            baths = 0.0
        else:
            beds = 3.0
            baths = 2.0
        pool = 'No info'
        fireplace = 'No info'
        parking = 'No info'
        heating = 'No info'

    left_column, right_column = st.columns([2, 8])
    pressed = left_column.button('Get the price!')

    if pressed:
        house = get_transformed_params(path, df, property_type, baths, fireplace, city, sqft, zip, beds, state, pool, heating, parking)
        value = get_estimation(path, house)
        left_column, right_column = st.columns([2, 10])
        text_value = f'<p style="font-family:sans-serif; color:#B64004; font-size: 35px;">${value:,d}</p> '
        left_column.markdown(text_value, unsafe_allow_html=True)
        text_comment = f'<p style="font-family:sans-serif; color:#B64004; font-size: 35px;">     -- HERE IS THE ' \
                       f'PRICE FOR YOUR ENTRY!</p> '
        right_column.markdown(text_comment, unsafe_allow_html=True)
        st.markdown('##### **Compare it to other properties below:**')

        left_column, right_column = st.columns(2)

        # First barchart
        fig_1 = bar_chart_types(df, state, city, zip, value)
        left_column.plotly_chart(fig_1, use_container_width=True)

        # Second chart
        fig_2 = bar_chart_state_city(df, state, city, zip, property_type)
        right_column.plotly_chart(fig_2, use_container_width=True)

        st.markdown('##### **See properties on map:**')
