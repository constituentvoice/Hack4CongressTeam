from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper, exc, backref
from sqlalchemy import event

db = SQLAlchemy()
Base = db.Model
Column = db.Column
Table = db.Table
Integer = db.Integer
SmallInteger = db.SmallInteger
Float = db.Float
ForeignKey = db.ForeignKey
String = db.String
Date = db.Date
DateTime = db.DateTime
Enum = db.Enum
Text = db.Text
Boolean = db.Boolean
relationship = db.relationship
backref = db.backref
joinedload = db.joinedload
and_ = db.and_
or_  = db.or_


class User(Base):
	__table__ = 'Constituent'
	id = Column(Integer, primary_key=True)
	cell = Column(String(512))
	address = Column(String(512))

class Question(Base):
	__table__ = 'Question'
	id = Column(Integer, primary_key=True)
	text = Column(String(512))

class Response(Base):
	__table__ = 'Response'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship('User',backref='user')
	text = Column(String(512))
	question_id = Column(Integer, ForeignKey('question.id'))
	question = relationship('Question', backref='responses')

class TextSession(Base):
	__table__ = 'text_session'

	id = Column(Integer,primary_key=True)
	message_state = Column(String(255))
	address = Column(String(255))
	lat = Column(Float)
	lon = Column(Float)
	cell = Column(String(255))
	state = Column(String(2))
	district = Column(Integer)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship('User',backref='textsession')

