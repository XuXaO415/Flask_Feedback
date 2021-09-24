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
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password and return user"""
        
        hashed = bcrypt.generate_password_hash(password)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        
        #return all instances of a user w/username and hashed password
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod 
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct. 
        Return user is valid; else return false"""
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            #return user instance
            return user
        else:
            return False




