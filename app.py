from flask import Flask, render_template, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
import pdb


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SoMeSoRTaSeCrEt**1110010"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


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
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session["username"] = username

        # On successful login, redirect to secret page
        # return redirect("/secret")
        # change /secret to /users/{username}
        return redirect ("/users/{username")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Shows form, authenticates and logs in user"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        
        # .authenticate will return a user or False
        user = User.authenticate(username, pwd)

        if user:
            session["username"] = username
            flash(f"Welcome back {username}!")
            # return render_template("secret.html")
            # return redirect("/secret")
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Oops, something went wrong"]

    return render_template("login.html", form=form)


# @app.route("/secret")
# def secret_page():

#     if "username" not in session:
#         flash("Sorry, you are in the wrong place!")
#         return redirect("/")
#     else:
#         return render_template("secret.html")


@app.route("/logout/")
def logout():
    """Logs user out and redirects to /"""
    # pdb.set_trace()

    session.pop("username")
    # db.session.commit()
    flash("You have successfully logged out.")

    return redirect("/")


@app.route("/users/<username>")
def user_info(username):
    """Shows info about a user except for their password"""
    if session["username"] != username:
        return redirect("/login")

    user = User.query.get_or_404(username)
    return render_template("user_info.html", user=user)
    
    
    
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Completely deletes a user and their feedback"""
    if session["username"] != username:
        return redirect("/login")

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/")
    

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """User is able to add feedback"""
    
    if session["username"] != username:
        return
    form = FeedbackForm()
    if not form.validate_on_submit():
        return render_template("add_feedback.html", form=form)

    title = form.title.data
    content = form.content.data

    feedback = Feedback(title=title, content=content, username=username)
    db.session.add(feedback)
    db.session.commit()

    return redirect(f"/users/{username}")
            
        
