import streamlit as st
import warnings

# Encryption
import hashlib
from path import get_hash

# Body
from house_prices_app import app_body
warnings.filterwarnings("ignore")


if __name__ == '__main__':
    st.set_page_config(layout='wide', page_icon=":house:", page_title='House pricing app')

    # Path for colab
    path_1 = '/content/drive/MyDrive/transport_costs_app/'

    # Path for local host (current folder)
    path_2 = ''

    """
    # US House Pricing Platform
    """

    st.markdown('### Using this app you can get the price estimation for various properties types')

    with st.sidebar.expander("Please enter password here:"):
        password = st.text_input("Password:", value="", type='password')

    if hashlib.sha1(password.encode('utf-8')).hexdigest() == get_hash():
        # try:
        app_body()
        # except:
        #     print('Что за фигня!')


    else:
        st.sidebar.markdown("### Password is incorrect!")

