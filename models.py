"""Database models."""
import os
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


# database_path = "postgres://{}/{}".format('localhost:5432', database_name)

database_path = os.environ.get('DATABASE_URL')
if not database_path:
	database_name = 'todoapp'
	database_path = 'postgresql://jaimeaznar@{}/{}'.format(
		'localhost:5432', database_name)

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class User(UserMixin, db.Model):
	"""User account model."""
	__tablename__ = 'userlogin'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, unique=False)
	email = db.Column(db.String(40), unique=True, nullable=False)
	password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
	task = db.relationship("Task", back_populates="userlogin", cascade="all, delete, delete-orphan", passive_deletes=True)

	def set_password(self, password):
		"""Create hashed password."""
		self.password = generate_password_hash(password, method='sha256')

	def check_password(self, password):
		"""Check hashed password."""
		return check_password_hash(self.password, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Task(db.Model):
	__tablename__ = 'task'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String, nullable=False)
	state = db.Column(db.Boolean, unique=False, default=False)
	# relationship
	user_id = db.Column(db.Integer,db.ForeignKey('userlogin.id',ondelete='CASCADE'))

	userlogin = db.relationship("User", back_populates="task")

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self):
		db.session.commit()
