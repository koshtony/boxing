import streamlit as st
import pandas as pd
import sqlite3
import time
from PIL import Image
from organ_sup import menu2
from items import gui
#import random
def menu():
    gui()
    col1,col3=st.columns((1,1))
    # create selection menu
    exp=col1.expander("Employee field")
    exp.write("""**About**""")
    radc1 = exp.selectbox("options",["fetch","add","edit","delete"])

    # saving employee infos
    if radc1=="add":
        id_no=exp.text_input("National id Number")
        name=exp.text_input("full name")
        gender=exp.selectbox("Gender",["Male","Female",""])
        birth=exp.date_input("Date of birth")
        doj=exp.date_input("date of joining")
        resign=exp.date_input("date of resigning")
        comp=exp.text_input("company")
        Dep=exp.text_input("Department")
        post=exp.text_input("Post Title")
        role=exp.text_input("Role name")
        status=exp.selectbox("Status",["working","leave","Resigned"])
        attr=exp.text_input("Job attributes")
        bank=exp.text_input("Bank name")
        bank_no=exp.text_input("Bank Card Number")
        Nation=exp.text_input("Nationality")
        addr=exp.text_input("Address")
        Emerg=exp.text_input("Emergency contact number")
        marital=exp.selectbox("Marital status",["Married","Single",""])
        edu=exp.selectbox("Education Level",["Primary school","High school","Bachelors","Masters"])
        major=exp.text_input("Major")
        gradu=exp.date_input("Graduation date")
        salary=exp.text_input("Salary")
        remark=exp.text_area("remark")
        if exp.button("ADD INFO"):
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)
            add_emp(id_no,name,gender,birth,doj,resign,comp,
            Dep,post,role,status,attr,bank,bank_no,Nation,
            addr,Emerg,marital,edu,major,gradu,salary,remark)

    # search employee by id
    elif radc1=="fetch":
        # input search by employee id
        emp_rad=exp.radio("",["All","filter"])
        if emp_rad=="All":
            col1.dataframe(fetch_emp())
        elif emp_rad=="filter":
            search=exp.text_input("search by id")
            if exp.button("fetch"):
                p=col1.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    p.progress(i+1)
                data=fetch_emp()
                d_f=data[data["empid"]==int(search)]
                col1.dataframe(d_f)
    elif radc1=="edit":
        # input for id to edit
        edit_id=exp.text_input("edit employee id")
        change=exp.selectbox("field to edit",["idno","name","gender","DOB","DOJ","DOS"
        ,"company","Department","post","role","status","job_attribute","Bank","bank_no",
        "nationality","address","emergency_no","marital_status","education","major","DOG","salary","remark"])
        sets=exp.text_input("new value")
        if exp.button("edit"):
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)
            edit_emp(change,sets,edit_id)

    elif radc1=="delete":
        emp_id=exp.text_input("employee id to delete")
        p=st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            p.progress(i+1)
        st.balloons()
        delete_emp(emp_id)
    menu2(col1,col3)



def add_emp(id_no,name,gender,birth,doj,resign,comp,
Dep,post,role,status,attr,bank,bank_no,Nation,
addr,Emerg,marital,edu,major,gradu,salary,remark):
    # sqlite add employee info code here
    conn=sqlite3.connect("organisation.db")
    con=conn.cursor()
    con.execute("create table if not exists employees(empid integer primary key autoincrement,idno integer,name text,gender string,DOB date,DOJ date,DOS date,company string,Department string,post string,role string,status string,job_attribute string,bank string,bank_no string,nationality string,address string,emergency_no string,marital_status string,education string,major string,DOG date,salary float,remark text)")
    con.execute("insert into employees (idno,name,gender,DOB,DOJ,DOS,company,Department,post,role,status,job_attribute,Bank,bank_no,nationality,address,emergency_no,marital_status,education,major,DOG,salary,remark) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id_no,name,gender,birth,doj,resign,comp,Dep,post,role,status,attr,bank,bank_no,Nation,addr,Emerg,marital,edu,major,gradu,salary,remark,))
    conn.commit()


def fetch_emp():
    # sqlite fetch code here
    conn=sqlite3.connect("organisation.db")
    data=pd.read_sql_query("select *from employees",conn)

    return data

def edit_emp(val,set,id):
    # sqlite edit code
    conn=sqlite3.connect("organisation.db")
    con=conn.cursor()
    cmd="update employees set "+str(val)+" =? "+"where empid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_emp(id):
     # delete employee by id.
     conn=sqlite3.connect("organisation.db")
     con=conn.cursor()
     con.execute("delete from employees where empid=?",(id,))
def get_emp_id(id):
    connx=sqlite3.connect("organisation.db")
    emp_data=pd.read_sql_query("select *from employees",connx)
    return emp_data.loc[emp_data["empid"]==id]["name"].to_list()[0]
