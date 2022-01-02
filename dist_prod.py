import streamlit as st
import sqlite3
import pandas as pd
import time
def dist_menu():
    c1,c2=st.columns((1,1))
    pander1=c1.expander("Fetch")
    fetch_r=pander1.radio("",["All","filter"])
    if fetch_r=="filter":
        id=pander1.text_input("Fetch by pid")
        if pander1.button("fetch"):
            data=fetch_info()
            f_data=data[data["pid"]==int(id)]
            st.write("--fetching")
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)

            st.dataframe(f_data)
    elif fetch_r=="All":
        st.dataframe(fetch_info())
    pander=c1.expander("Add info")
    price=pander.text_input("product price")
    quantity=pander.text_input("Quantity")
    region=pander.selectbox("Region",["Central","Rift"])
    town=pander.selectbox("Town",["Nairobi","Mombasa"])
    shop=pander.text_input("Shop Name")
    desc=pander.text_area("Product description")
    if pander.button("Confirm"):
            add_info(price,quantity,desc,region,town,shop)
    pander3=c2.expander("Delete")
    d_id = pander3.text_input("pid")
    if pander3.button("Delete"):
        p=st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            p.progress(i+1)

        delete_info(d_id)
    pander4=c2.expander("Edit")
    edit_id=pander4.text_input("Edit by pid")
    change=pander4.selectbox("Field to edit",["quantity","region","town","shop"])
    set=pander4.text_input("New Value")
    if pander4.button("Edit"):
        p=st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            p.progress(i+1)

        edit_info(change,set,edit_id)

def add_info(price,quantity,desc,region,town,shop):
    # adding distribution data
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("create table if not exists dist_prod(pid integer primary key autoincrement,price float,quantity float,description text,region text,town text,shop text,foreign key (pid) references orgsupply(pid))")
    con.execute("insert into dist_prod (price,quantity,description,region,town,shop) values (?,?,?,?,?,?)",(price,quantity,desc,region,town,shop))
    conn.commit()

def fetch_info():
    # extract distribution data
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("select *from dist_prod")
    values=con.fetchall()
    names=["pid","price","quantity","description","region","town","shop"]
    val_dict={}
    for i in range(len(names)):
        val_dict[names[i]]=values[0][i]

    return pd.DataFrame(val_dict,index=[0])

def edit_info(val,set,id):
    # edit distribution information
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    cmd="update dist_prod set "+str(val)+" =? "+"where pid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_info(id):
    # delete distribution info by id
    conn=sqlite3.connect("organs.db")
    con=conn.cursor()
    con.execute("delete from dist_prod where pid=?",(id,))
    conn.commit()
