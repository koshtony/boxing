from flask import Flask,render_template,redirect,request,flash,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager as l
from flask_wtf import FlaskForm
import sqlite3
import pandas as pd
from items import fetch
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError
from wtforms import StringField,IntegerField,SelectField,SubmitField,PasswordField,BooleanField,TextAreaField
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required
app=Flask(__name__,template_folder='template')
key='@boxing'
app.config['SECRET_KEY']=key
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///orders.db'
data=SQLAlchemy(app)
lm=l(app)
@lm.user_loader
def load_user(s_id):
    return member.query.get(int(s_id))
class member(data.Model,UserMixin):
    id=data.Column(data.Integer,primary_key=True)
    eid=data.Column(data.Integer,nullable=False)
    password=data.Column(data.String,nullable=False)
    image=data.Column(data.String(50),nullable=False,default='default.jpg')
    relt=data.relationship('orders',backref='members',lazy=True)
    def __repr__(self):
        return str(self.id)
class logform(FlaskForm):
    eid=StringField('Employee Id',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=6,max=30)])
    remember=BooleanField('remember me')
    submit=SubmitField('login')
class orders(data.Model):
    id=data.Column(data.Integer,primary_key=True)
    eid=data.Column(data.Integer,nullable=True)
    fname=data.Column(data.String(50),nullable=True)
    phone=data.Column(data.String(20),nullable=True)
    item=data.Column(data.String(20),nullable=True)
    size=data.Column(data.Integer,nullable=True)
    quant=data.Column(data.Integer,nullable=True)
    desc=data.Column(data.Text,nullable=True)
    quantity=data.Column(data.String(10),nullable=True)
    sprice=data.Column(data.Integer,nullable=True)
    dprice=data.Column(data.Integer,nullable=True)
    ddate=data.Column(data.String(20),nullable=True)
    customer=data.Column(data.String(50),nullable=True)
    cphone=data.Column(data.String(20),nullable=True)
    town=data.Column(data.String(50),nullable=True)
    loc=data.Column(data.Text,nullable=True)
    date=data.Column(data.DateTime,nullable=False,default=datetime.utcnow)
    s_id=data.Column(data.Integer,data.ForeignKey('member.eid'),nullable=False)
    def __repr__(self):
        return str(self.id)
class orderform(FlaskForm):
    fnames=StringField("SR full name",validators=[DataRequired()])
    phone=StringField("SR phone number",validators=[DataRequired()])
    item=SelectField("Item",choices=[(i,i) for i in fetch()["name"].tolist()] ,validators=[DataRequired()])
    size=IntegerField("Item size",validators=[DataRequired()])
    quant=IntegerField("Quantity",validators=[DataRequired()])
    desc=TextAreaField("Description",validators=[DataRequired()])
    sprice=IntegerField("Selling Price",validators=[DataRequired()])
    dprice=IntegerField("Delivery Price",validators=[DataRequired()])
    ddate=StringField("Delivery Date",validators=[DataRequired()])
    customer=StringField("Customer Name",validators=[DataRequired()])
    cphone=StringField("Customer Phone No",validators=[DataRequired()])
    town=StringField("Town",validators=[DataRequired()])
    loc=TextAreaField("Describe location",validators=[DataRequired()])
    submit=SubmitField('Order')
    #phone=PhoneNumberField("phone number",validators=[DataRequired()])
@app.route('/',methods=['GET','POST'])
def login():

    form=logform()
    if form.validate_on_submit():
        credentials=member.query.filter_by(eid=form.eid.data).first()
        if credentials and credentials.password:
            login_user(credentials,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'invalid email or password','danger')
    return render_template('login.html',form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form=orderform()
    if form.validate_on_submit:
        print(form.phone.data)
        savings=orders(eid=current_user.eid,fname=form.fnames.data,phone=form.phone.data,
        item=form.item.data,size=form.size.data,quantity=form.quant.data,desc=form.desc.data,sprice=form.sprice.data,
        dprice=form.dprice.data,ddate=form.ddate.data,customer=form.customer.data,cphone=form.cphone.data,
        town=form.town.data,loc=form.loc.data,members=current_user)
        data.session.add(savings)
        data.session.commit()
        return redirect(url_for('login'))
    return render_template('orders.html',form=form)


if __name__=="__main__":
    app.run(debug=True)
