import streamlit as st
from organ_emp import menu
from PIL import Image
from dist_prod import dist_menu
# created navigation menu using radio button
st.get_option("theme.textColor")
page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
rad1 = st.sidebar.radio("menu",["ORGANISATION","DISTRIBUTION MANAGEMENT",
                "SUPPLY MANAGEMENT","CUSTOMER INFO","MARKET INFO"])
if rad1=="ORGANISATION":
    menu()
elif rad1=="DISTRIBUTION MANAGEMENT":
    dist_menu()
