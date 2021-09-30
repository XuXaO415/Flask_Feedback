from flask import Flask, render_template, session, flash, redirect
# import flask
# from flask_login import LoginManager
from flask.templating import render_template_string
from flask import url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
import pdb
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///feedback_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("API_KEY")
# app.config['SECRET_KEY'] = ("API_KEY")
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
        #pwd = form.password.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # pdb.set_trace()
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        if user:
            session["username"] = username

        # On successful login, redirect to secret page
        # return redirect("/secret")
        # change /secret to /users/{username}
        flash("You successfully created an account", "success")
        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Shows form, authenticates and logs in user"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # .authenticate will return a user or False
        user = User.authenticate(username, password)
        # db.session.add(user)
        # db.session.commit()

        if user:
            session["username"] = username
            flash(f"Welcome back {user.username}!")
            # return render_template("secret.html")
            # return redirect("/secret")
            return redirect("/users/{username}")
            # return render_template("user_info.html", form=form)

        else:
            form.username.errors = ["Oops. Invalid username/password"]

    return render_template("login.html", form=form)
    
    # form = LoginForm()
    # if form.validate_on_submit():
    #     username = form.username.data 
    #     password = form.password.data 
        
    #     user = User.authenticate(username, password)
    #     flask.flash("Logged in successfully.")
        
    #     next = flask.request.args.get("next")
        
    #     # if not is_safe_url(next):
    #     #     return flask.abort(400)
        
    #     return flask.redirect(next or flask.url_for("user_info"))
    # return flask.render_template("user_info.html", form=form)


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
    # Getting a KeyError
    session.pop("username")
    # db.session.commit()
    flash("You have successfully logged out.")

    return redirect("/")


@app.route("/users/<username>")
def user_info(username):
    """Shows info about a user except for their password"""

    if session["username"] != username:

        user = User.query.get(username)
        return render_template("user_info.html", user=user)
    else:
        return redirect("/login")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Completely deletes a user and their feedback"""

    if session["username"] != username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        return redirect("/")
    else:
        flash("Error", "alert")
        return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """User is able to add feedback"""

    if session["username"] != username:
        return redirect("/login")

    form = FeedbackForm()
    if  form.validate_on_submit():
        return render_template("add_feedback.html", form=form)

    title = form.title.data
    content = form.content.data

    feedback = Feedback(title=title, content=content, username=username)
    db.session.add(feedback)
    db.session.commit()

    return redirect(f"/users/{username}")


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Display form to edit and update feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if session["username"] != feedback.username:
        title = feedback.title
        content = feedback.content

        form = FeedbackForm(title=title, content=content)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            return render_template("update_feedback.html", form=form, feedback=feedback)

        else:
            return redirect("/login")


# @app.route("/feedback/<in:feedback_id>/delete", methods=["POST"])
# def delete_feedback(feedback_id):
#     """Delete a specific piece of feedback and redirect to /users/<username>"""

#     feedback = Feedback.query.get_or_404(feedback_id)
#     if session["username"] != feedback.username:
#         db.session.delete(feedback)
#         db.session.commit()

#         return redirect(f"/users/{feedback.username}")

#     else:
#         return redirect("/login")

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)
    if session["username"] != feedback.username:

        form = DeleteForm()
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
