import warnings
import pandas as pd
import numpy as np
# import sklearn
# from sklearn.preprocessing import OrdinalEncoder, RobustScaler
import catboost

import pickle
import plotly.graph_objects as go
import base64

from plotly.subplots import make_subplots
from io import BytesIO

warnings.filterwarnings("ignore")


def df_preparation(path):
    df = pd.read_csv(f'{path}data_processed.csv')
    states = list(df.state.unique())
    types = list(df.propertyType.unique())
    heatings = list(df.Heating.unique())
    states.sort()
    states_cities = {}
    for state in states:
        cities = list(df[df['state'] == state].city.unique())
        cities.sort()
        states_cities[state] = cities
    cities_zip = {}
    for city in list(df.city.unique()):
        zips = list(df[df['city'] == city].zipcode.unique())
        zips.sort()
        cities_zip[city] = zips

    return df, states, types, heatings, states_cities, cities_zip


# Parameters

def get_transformed_params(path, df, property_type, baths, fireplace, city, sqft, zip, beds, state, pool, heating, parking,
                           status='FOR SALE'):
    house = pd.DataFrame(columns=['status', 'propertyType', 'baths', 'fireplace', 'city', 'sqft', 'zipcode', 'beds',
                                  'state', 'PrivatePool', 'Heating', 'Parking'],
                         data=[[status, property_type, baths, fireplace, city, sqft, zip,
                                beds, state, pool, heating, parking]])
    # If no city or zipcode
    if house['city'].values[0] == 'No city/other':
        house['city'] = df[df['state'] == state].city.value_counts().keys()[0]
        house['zipcode'] = df[df['city'] == house['city'].values[0]].zipcode.value_counts().keys()[0]

    if house['zipcode'].values[0] == 'No zip/other':
        house['zipcode'] = df[df['city'] == city].zipcode.value_counts().keys()[0]

    # Price per sqft and max rating
    house['zipcode'] = house['zipcode'].astype('int')
    house['max_rating'] = df[df['zipcode'] == house['zipcode'].values[0]].max_rating.max()
    house['Price_sqft_state'] = df[df['state'] == house['state'].values[0]].Price_sqft_state.mean()
    house['Price_sqft_city'] = df[df['city'] == house['city'].values[0]].Price_sqft_city.mean()
    house['Price_sqft_zip'] = df[df['zipcode'] == house['zipcode'].values[0]].Price_sqft_zip.mean()

    # Apply hard boolean coding
    house['PrivatePool'] = house['PrivatePool'].apply(lambda x: 1 if x == 'Yes' else 0)
    house['Parking'] = house['Parking'].apply(lambda x: 1 if x != 'No' else 0)
    house['fireplace'] = house['fireplace'].apply(lambda x: 1 if x == 'Yes' else 0)
    house['Heating'] = house['Heating'].apply(lambda x: 'OTHER' if x == 'No info' else x)

    # UnPickle encoding
    enc_ord = pickle.load(open(f'{path}ord_enc.pkl', 'rb'))
    house['zipcode'] = house['zipcode'].astype('str')
    house[['zipcode', 'city', 'state', 'propertyType', 'Heating', 'status']] = enc_ord.transform(
        house[['zipcode', 'city', 'state', 'propertyType', 'Heating', 'status']])

    # Data types
    house['sqft'] = house['sqft'].astype('float')

    # Logarithms
    house[['sqft', 'Price_sqft_state', 'Price_sqft_city', 'Price_sqft_zip']] = np.log(
        house[['sqft', 'Price_sqft_state', 'Price_sqft_city', 'Price_sqft_zip']])

    # Data normalization
    numeric = ['baths', 'sqft', 'beds', 'max_rating', 'Price_sqft_state', 'Price_sqft_city', 'Price_sqft_zip']
    scaler = pickle.load(open(f'{path}robust_scaler.pkl', 'rb'))
    house[numeric] = scaler.transform(house[numeric])

    return house


def get_estimation(path, house):
    model = pickle.load(open(f'{path}best_model.pkl', 'rb'))
    value = int(np.exp(model.predict(house))[0])
    return value


def to_excel(df):
    """
    Preprocess a dataframe and prepare it to be downloadable as Excel file
    :param df: dataframe
    :return: processed data
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output)
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link_excel(df, state, city, zip, property_type):
    """Generates a link allowing the data in a given panda dataframe to be downloaded as Excel file
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="House_prices_for_{state}_' \
           f'{city}_to_{zip}_{property_type}.xlsx">Download table as Excel</a> '
    return href


# Visualization part

# Colors
color_1 = '#5254c7'
color_2 = '#c75252'


def bar_chart_types(df_bar, state, city, zip, value, color=color_1):
    if zip != 'No zip/other' and len(df_bar[df_bar['zipcode'] == int(zip)]) > 2:
        df_bar = df_bar[df_bar['zipcode'] == int(zip)]
        title_input = str(zip)
        title_text = 'zipcode'
    elif city != 'No city/other' and len(df_bar[df_bar['city'] == city]) > 2:
        df_bar = df_bar[df_bar['city'] == city]
        title_input = str(city)
        title_text = 'city'
    else:
        df_bar = df_bar[df_bar['state'] == state]
        title_input = str(state)
        title_text = 'state'

    group = df_bar.groupby('propertyType').target.mean().reset_index()
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=group['propertyType'],
        y=group['target'],
        name=f"Avg price per type",
        marker_color=color
    )
    )

    fig.add_trace(go.Scatter(
        x=group['propertyType'],
        y=[value for i in range(len(group['propertyType']))],
        name="Estimated price",
        mode='lines',
        line=dict(color='#c75252', shape='spline', width=2, smoothing=1.3, dash='dash')
    )
    )

    # Here we modify the layout
    fig.update_layout(title_text=f"<b>Avg price per type, $ </b><br>For "
                                 f"{title_input} <i>{title_text}</i> </br>",
                      title_font_size=18,
                      xaxis_tickangle=-45,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(
                          yanchor="top",
                          xanchor="right"),
                      yaxis_range=[group['target'].min()-group['target'].min()*0.5, group['target'].max()]
                      )
    return fig


def bar_chart_state_city(df_bar, state, city, zip, property_type, color=color_1):

    df_bar = df_bar[df_bar['propertyType'] == property_type]

    if city != 'No city/other' and len(df_bar[df_bar['city'] == city]) > 2:
        if zip != 'No zip/other':
            df_bar = df_bar[df_bar['city'] == city]
            average = df_bar[df_bar['zipcode'] == zip]['target'].mean()
            group = df_bar.groupby('zipcode').target.mean().reset_index()
            group['zipcode'] = group['zipcode'].astype('str')

            plot_x_text = str(zip)
            plot_y_value = average
            title_input = str(city)
            title_text = 'zipcodes'

        else:
            df_bar = df_bar[df_bar['state'] == state]
            average = df_bar[df_bar['city'] == city]['target'].mean()
            group = df_bar.groupby('city').target.mean().reset_index()
            group['city'] = group['city'].astype('str')

            plot_x_text = str(city)
            plot_y_value = average
            title_input = str(state)
            title_text = 'cities'
    else:
        average = df_bar[df_bar['state'] == state]['target'].mean()
        group = df_bar.groupby('state').target.mean().reset_index()
        group['state'] = group['state'].astype('str')

        plot_x_text = str(state)
        plot_y_value = average
        title_input = 'US'
        title_text = 'states'

    # group = group[(group['target'] > average*0.5) & (group['target'] < average*2.5)]

    if len(group) > 7:
        targets = group['target'].to_list()
        targets.sort()
        idx = targets.index(average)
        targets = targets[idx - 3: idx + 4]
        group = group.loc[group['target'].isin(targets)]
        group = group.loc[group['target'] != average]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=group[list(group.columns)[0]],
        y=group['target'],
        name=f"Avg price per zipcode",
        marker_color=color
    )
    )

    fig.add_trace(go.Bar(
        x=[plot_x_text],
        y=[plot_y_value],
        name=f"{plot_x_text}",
        marker_color='#c75252'
        )
        )

    # Here we modify the layout
    fig.update_layout(title_text=f"<b>Avg price for similar {title_text}, $ </b><br>Type: "
                                 f"{property_type},  in {title_input} </br>",
                      title_font_size=18,
                      xaxis_tickangle=-45,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      yaxis_range=[group['target'].min()-group['target'].min()*0.5, group['target'].max()]
                      )
    return fig


def plot_map(df, state, city, zip, value, sqft, property_type):

    df_bar = df[df['propertyType'] == property_type]

    if city != 'No city/other' and len(df_bar[df_bar['city'] == city]) > 2:
        if zip != 'No zip/other':
            df_bar = df_bar[df_bar['zipcode'] == zip]

        else:
            df_bar = df_bar[df_bar['city'] == city]

    else:
        df_bar = df_bar[df_bar['state'] == state]

    sqft = float(sqft)
    if len(df_bar) > 20:
        targets = df_bar['target'].to_list()
        targets.sort()
        feets = df_bar['sqft'].to_list()
        feets.sort()

        array = np.asarray(targets)
        idx = (np.abs(array - value)).argmin()   # min closest value
        array_2 = np.asarray(feets)
        idx_2 = (np.abs(array_2 - sqft)).argmin()

        targets = targets[idx - 5: idx + 6]
        feets = feets[idx_2 - 5: idx_2 +6]
        df_bar = df_bar.loc[((df_bar['target'].isin(targets)) | (df_bar['sqft'].isin(feets)))]

    df_bar = df_bar[['propertyType', 'state', 'city', 'zipcode', 'sqft', 'beds', 'baths', 'target']].reset_index(drop=True)
    df_bar[['sqft', 'beds', 'baths', 'target']] = df_bar[['sqft', 'beds', 'baths', 'target']].astype(int)
    df_bar.rename(columns={"target": "price", "propertyType": "property_type"}, inplace=True)

    return df_bar
