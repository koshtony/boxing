from flask import Flask,render_template,redirect,request,flash,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager as l
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError
from wtforms import StringField,SelectField,SubmitField,PasswordField,BooleanField,TextAreaField
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required
app=Flask(__name__,template_folder='template')
key='@boxing'
app.config['SECRET_KEY']=key
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///suppliers.db'
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
    shop=data.Column(data.String(20),nullable=True)
    region=data.Column(data.String(50),nullable=True)
    quantity=data.Column(data.String(10),nullable=True)
    date=data.Column(data.DateTime,nullable=False,default=datetime.utcnow)
    typ=data.Column(data.String(50),nullable=True)
    s_id=data.Column(data.Integer,data.ForeignKey('member.eid'),nullable=False)
    def __repr__(self):
        return str(self.id)
class orderform(FlaskForm):
    fnames=StringField("full name",validators=[DataRequired()])
    phone=StringField("phone number",validators=[DataRequired()])
    item=StringField("Item to order",validators=[DataRequired()])
    shop=StringField("shop name",validators=[DataRequired()])
    region=StringField("Region",validators=[DataRequired()])
    quantity=StringField("Quantity(1kg,1.5kg etc)")
    typ=SelectField("order type",validators=[DataRequired()],choices=[
        ('Distributors','Distributors'),
        ('Retailer','Retailer'),
        ('others','others')])
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
    return redirect(url_for('home'))
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form=orderform()
    if form.validate_on_submit():
        print(form.phone.data)
        savings=orders(eid=current_user.eid,fname=form.fnames.data,phone=form.phone.data,
        item=form.item.data,shop=form.shop.data,region=form.region.data,
        quantity=form.quantity.data,typ=form.typ.data,members=current_user)
        data.session.add(savings)
        data.session.commit()
    return render_template('orders.html',form=form)


if __name__=="__main__":
    app.run(debug=True)
