from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = "users"
        
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.VARCHAR(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    feedbacks = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")
    
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password and return user"""
        
        hashed = bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        
        #return all instances of a user w/username and hashed password
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod 
    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct. 
        Return user is valid; else return false"""
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            #return user instance
            return u
        else:
            return False
        

class Feedback(db.Model):
    __tablename__ = "feedbacks"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey("users.username", ondelete="Cascade"), nullable=False )
    