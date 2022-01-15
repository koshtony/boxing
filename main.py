import streamlit as st
import streamlit_authenticator as stauth
from organ_emp import menu
from PIL import Image
from dist_prod import dist_menu
from auth import logs,retrv_log
# created navigation menu using radio button
st.get_option("theme.textColor")
#creating login page
def back_im():
    background = Image.open('back.jpeg')
    st.image(background, width=650)

ex=st.expander("COMPANY INFO")
ex.write("Things to note")
log_ex=st.sidebar.expander("Create User")
name=log_ex.text_input("Name")
eid=log_ex.text_input("Employee Id")
pwd=log_ex.text_input("Create Password",type="password")
pwd2=log_ex.text_input("Confirm Password",type="password")
if log_ex.button("Create Username"):
    if pwd!=pwd2:
        st.write("password not same")
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
elif login_status==False:
    back_im()
    st.sidebar.error("incorrect password")
elif login_status==None:
    back_im()
    st.sidebar.warning("insert Username and password")
