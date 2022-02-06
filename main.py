import streamlit as st
import streamlit_authenticator as stauth
from organ_emp import menu
from PIL import Image
from dist_prod import dist_menu
from auth import logs,retrv_log
from organ_emp import fetch_emp
from supplier import incoming,download
# created navigation menu using radio button
st.get_option("theme.textColor")
#creating login page
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
def back_im():
    background = Image.open('back.jpeg')
    st.image(background, width=650)

ex=st.expander("MENU")
ex.write("Things to note")
ex.write("Order Here [link](https://boxingsales.herokuapp.com/home)")
log_ex=st.sidebar.expander("Create User")
name=log_ex.text_input("Name")
eid=log_ex.text_input("Employee Id")
pwd=log_ex.text_input("Create Password",type="password")
pwd2=log_ex.text_input("Confirm Password",type="password")
info=fetch_emp()

if log_ex.button("Create User"):
    if pwd!=pwd2:
        st.sidebar.write("password doesn't match")
    elif info[info["emp id"]==int(eid)].shape[0]==0:
        st.sidebar.error("Employee id not recognised")
    else:
        logs(name,eid,pwd2)
        st.write("User created successfully")
names,usernames,passwords=retrv_log()
usernames=[str(i) for i in usernames]
passwords = stauth.hasher(passwords).generate()
logins= stauth.authenticate(names,usernames,passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
name,login_status = logins.login('Login','sidebar')
if login_status==True:
    rad1 = st.sidebar.radio("menu",["ORGANISATION","DISTRIBUTION MANAGEMENT",
                    "SUPPLY MANAGEMENT","CUSTOMER INFO","MARKET INFO"])
    if rad1=="ORGANISATION":
        menu()
    elif rad1=="DISTRIBUTION MANAGEMENT":
        dist_menu()
    elif rad1=="SUPPLY MANAGEMENT":
        st.header("Incoming Orders")
        st.dataframe(incoming()[0])
        file=download(incoming()[0])
        st.download_button(
        "Export",
        file,
        "incoming_orders.csv",
        "text/csv",
        key="download-csv"
        )

elif login_status==False:
    back_im()
    st.sidebar.error("incorrect password")
elif login_status==None:
    back_im()
    st.sidebar.warning("insert Username and password")
