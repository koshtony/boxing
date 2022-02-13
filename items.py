import streamlit as st
import pandas as pd
import sqlite3 as sq
def gui():
    drop=st.expander("Items")
    opt=drop.selectbox("",["fetch","Add","Delete"])
    if opt=="fetch":
        st.dataframe(fetch())
    elif opt=="Add":
        name=drop.text_input("Item Name")
        date=drop.date_input("creation date")
        category=drop.text_input("Item Category")
        family=drop.text_input("Item Family")
        remark=drop.text_area("remark")
        if drop.button("Add"):
            add(name,date,category,family,remark)
            drop.info("item added successfully")
    elif opt=="Delete":
        name=drop.text_input("item to delete")
        if drop.column("Delete Item"):
            delete(name)
            drop.info("Item deleted successfully")
def add(name,date,category,family,remark):
    conn=sq.connect("item.db")
    con=conn.cursor()
    con.execute("create table if not exists prod(name string,created date,category string,family string,remark text)")
    con.execute("insert into prod (name,created,category,family,remark) values(?,?,?,?,?)",(name,date,category,family,remark))
    conn.commit()
def fetch():
    conn=sq.connect("item.db")
    df=pd.read_sql_query("select *from prod",conn)
    return df
def delete(name):
    conn=sq.conect("item.db")
    cur=conn.cursor()
    cur.execute("delete from prod where name=?",(name,))
