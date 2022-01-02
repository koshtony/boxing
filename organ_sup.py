import streamlit as st
import sqlite3
import pandas as pd
import time
def menu2(col1,col2,col3):
    exp=col3.expander("Supply field")
    radc2=exp.selectbox("",["fetch","add","edit","delete"])
    if radc2=="add":
        # add product info
        name=exp.text_input("product name")
        desc=exp.text_input("product descriptions")
        if exp.button("add product"):
            exp.write("---Adding product--->")
            progress=exp.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            add_prod(name,desc)
            exp.write("product Added successfully")
    elif radc2=="fetch":
        # input search by product id
        s_fetch_r=exp.radio("",["All","fetch"])
        if s_fetch_r=="fetch":
            search=exp.text_input("search by product id")
            if exp.button("fetch product"):
                exp.write("searching product")
                progress=exp.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i+1)
                s_fetch_d=fetch_prod()
                s_f_fetch_d=s_fetch_d[s_fetch_d["pid"]==int(search)]
                col3.dataframe(s_f_fetch_d)
        elif s_fetch_r=="All":
            col3.dataframe(fetch_prod())


    elif radc2=="edit":
        # input edit by product id
        edit_p_id=exp.text_input("edit by product id")
        change=exp.selectbox("field to edit",["name","desc"])
        sets=exp.text_input("new value")
        if exp.button("edit product"):
            progress=exp.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            edit_prod(change,sets,edit,p_id)
    elif radc2=="delete":
        p_id=exp.text_input("product id to delete")
        if exp.button("delete product"):
            exp.write("----deleting product --->")
            progress=exp.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            delete_prod(p_id)
def add_prod(name,desc):
    # sqlite add employee info code here
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("create table if not exists orgsupply(pid integer primary key autoincrement,name text,description text)")
    con.execute("insert into orgsupply (name,description) values (?,?)",(name,desc,))
    conn.commit()


def fetch_prod():
    # sqlite fetch code here
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("select *from orgsupply")
    values=con.fetchall()
    names=["pid","name","description"]

    return pd.DataFrame(values,columns=names)

def edit_prod(val,set,id):
    # sqlite edit code
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    cmd="update orgsupply set "+str(val)+" =? "+"where pid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_prod(id):
     # delete products by id.
     conn=sqlite3.connect("organs.db")
     con=conn.cursor()
     con.execute("delete from orgsupply where pid=?",(id,))
