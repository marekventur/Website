from main import db
from flask.ext.login import UserMixin
import bcrypt
import os
import base64
from datetime import datetime, timedelta


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    name = db.Column(db.String, nullable=False, index=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    arrivals = db.Column(db.Boolean, default=False, nullable=False)
    phone = db.Column(db.String, nullable=True)
    tickets = db.relationship('Ticket', lazy='dynamic', backref='user', cascade='all, delete, delete-orphan')
    payments = db.relationship('Payment', lazy='dynamic', backref='user', cascade='all')

    def __init__(self, email, name):
        self.email = email
        self.name = name

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.hashpw(password.encode('utf8'), self.password) == self.password

    def __repr__(self):
        return '<User %s>' % self.email

class PasswordReset(db.Model):
    __tablename__ = 'password_reset'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String, nullable=False)

    def __init__(self, email):
        self.email = email
        self.expires = datetime.utcnow() + timedelta(days=1)

    def new_token(self):
        self.token = base64.urlsafe_b64encode(os.urandom(5 * 3))

    def expired(self):
        return self.expires < datetime.utcnow()
