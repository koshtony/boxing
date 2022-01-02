import streamlit as st
from organ_emp import menu
from PIL import Image
from dist_prod import dist_menu
# created navigation menu using radio button
st.get_option("theme.textColor")
rad1 = st.sidebar.radio("menu",["ORGANISATION","DISTRIBUTION MANAGEMENT",
                "SUPPLY MANAGEMENT","CUSTOMER INFO","MARKET INFO"])
if rad1=="ORGANISATION":
    menu()
elif rad1=="DISTRIBUTION MANAGEMENT":
    dist_menu()
