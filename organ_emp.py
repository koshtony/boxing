import streamlit as st
import pandas as pd
import sqlite3
import time
from PIL import Image
from organ_sup import menu2
#import random
def menu():
    col1,col2,col3=st.columns((2,1,2))
    # create selection menu
    exp=col1.expander("Employee field")
    exp.write("""**About**""")
    radc1 = col1.selectbox("options",["fetch","add","edit","delete"])
    # saving employee infos
    if radc1=="add":
        name=col1.text_input("full name")
        id_no=col1.text_input("National id Number")
        age=col1.text_input("age")
        date=col1.date_input("date of joining")
        if col1.button("ADD INFO"):
            try:
                add_emp(name,id_no,age,date)
            except Exception as e:
                st.write(e)
    # search employee by id
    elif radc1=="fetch":
        # input search by employee id
        search=col1.text_input("search by id")
        if col1.button("fetch"):
            st.write(fetch_emp(search))
    elif radc1=="edit":
        # input for id to edit
        edit_id=col1.text_input("edit employee id")
        change=col1.selectbox("field to edit",["name","idno","Date","age"])
        sets=col1.text_input("new value")
        if col1.button("edit"):
            with st.spinner("--editimg"):
                edit_emp(change,sets,edit_id)

    elif radc1=="delete":
        emp_id=col1.text_input("employee id to delete")
        delete_emp(emp_id)

    menu2(col1,col2,col3)



def add_emp(name,id,age,date):
    # sqlite add employee info code here
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("create table if not exists organisation(empid integer primary key autoincrement,name text,idno integer,age integer, Date date)")
    con.execute("insert into organisation (name,idno,age,date) values (?,?,?,?)",(name,id,age,date,))
    conn.commit()


def fetch_emp(id):
    # sqlite fetch code here
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("select *from organisation where empid=?",(id,))
    values=con.fetchall()
    names=["emp id","name","id","age","joining date"]
    val_dict={}
    for i in range(len(names)):
        val_dict[names[i]]=values[0][i]

    return pd.DataFrame(val_dict,index=[0])

def edit_emp(val,set,id):
    # sqlite edit code
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    cmd="update organisation set "+str(val)+" =? "+"where empid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_emp(id):
     # delete employee by id.
     conn=sqlite3.connect("organs.db")
     con=conn.cursor()
     con.execute("delete from organisation where empid=?",(id,))
