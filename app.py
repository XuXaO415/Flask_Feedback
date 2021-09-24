from flask import Flask, render_template, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SoMeSoRTaSeCrEt**1110010"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def redirect():
    """Redirects to register page"""
    
    return redirect("/register")

    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Shows form and registers new user"""
    
    form = RegisterForm()
    
    if form.vlaidate_on_submit():
        username = form.username.data 
        password = form.password.data 
        email = form.email.data 
        first_name =form.first_name.data 
        last_name = form.last_name.data 
        
        
        
    
    return redirect("/secret")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Shows form, authenticates and logs in user"""
    
    form = LoginForm()
    
    return redirect("/secret")
