
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'user'

    username       = db.Column(db.String(20), primary_key = True)
    password     = db.Column(db.Text, nullable=False)
    email       = db.Column(db.String(50), nullable=False, unique=True)
    first_name    = db.Column(db.String(30), nullable=False)
    last_name     = db.Column(db.String(30),  nullable=False)
    feedbacks     = db.relationship("Feedback",cascade="all,delete")

    

    def __repr__(self):
        return f"username: {self.username}, password: {self.password}, email: {self.email},   first_name: {self.first_name}, last_name: {self.last_name}"

    def encrypt(password):
        encryptor=Bcrypt()
        hashed_value=encryptor.generate_password_hash(password)
        return hashed_value.decode("utf8")

    def authentication_ok(username, password):
        encryptor=Bcrypt()
        user = User.query.filter_by(username=username).first()
        if user and encryptor.check_password_hash(user.password, password):
            return True
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title       = db.Column(db.String(100), nullable=False)
    content     = db.Column(db.Text, nullable=False)
    username       = db.Column(db.String(20), db.ForeignKey('user.username'))

    

    def __repr__(self):
        return f"id: {self.id}, title: {self.title}, content: {self.content},   username: {self.username}"
        



    