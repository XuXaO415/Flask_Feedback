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
def homepage():
    """Redirects to register page"""
    
    return redirect("/register")

    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Shows form and registers new user"""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 
        email = form.email.data 
        first_name =form.first_name.data 
        last_name = form.last_name.data 
        
        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        
        #On successful login, redirect to secret page
        return redirect("/secret")
    
    else:
        return render_template("register.html", form=form)
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Shows form, authenticates and logs in user"""
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data
        
        #authenticate will return a user or False
        user = User.authenticate(username, password)
        
        if user:
            session["username"] = username 
            return redirect("/secret")
        
        else:
            form.username.errors = ["Oops, something went wrong"]
            
            return render_template("login.html", form=form)
        
    
    @app.route("/secret")
    def secret():
        if "username" in session:
            return render_template("secret.html")

        flash("You made it!")
        return redirect("/")
    
    @app.route("/logout")
    def logout():
        """Logs user out and redirects to /"""
        
        session.pop("username")
        
        return redirect("/")
