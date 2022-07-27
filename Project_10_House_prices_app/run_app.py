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

    """
    # US House Pricing Platform
    """

    st.markdown('### Using this app you can get the price estimation for various properties types')

    with st.sidebar.expander("Copy paste password 'Hi_pricing_app' here:"):
        password = st.text_input("Password:", value="", type='password')

    if hashlib.sha1(password.encode('utf-8')).hexdigest() == get_hash():
        app_body()

    else:
        st.sidebar.markdown("### Password is incorrect!")

