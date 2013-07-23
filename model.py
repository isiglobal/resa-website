"""
I considered using OO-inheritance with the ORM, but ultimately
want freedom to develop Pages independently of Articles without
having to do a schema migration.
"""

import datetime
import hashlib
import random
import string
import json

from sqlalchemy import Column, Integer, String, DateTime,\
						Boolean, Table, Text, ForeignKey,\
						Float

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

#from flask.ext.wtf import Form, BooleanField, TextField, \
#		PasswordField, validators

from database import Base

# association table
article_tags = Table('article_tags',
	Base.metadata,
	Column('article_id', Integer, ForeignKey('articles.id')),
	Column('tag_id', Integer, ForeignKey('tags.id')),
)

class Article(Base):
	__tablename__ = 'articles'
	id = Column(Integer, primary_key=True)

	datetime_added = Column(DateTime, nullable=True,
							default=datetime.datetime.now)
	datetime_edited = Column(DateTime, nullable=True)

	title = Column(String(1000)) # Eg. 'This is the Title of the Article'
	url_key= Column(String(1000)) # Shortened, eg. /article/'this-is-the-ti...'

	content_mkdown = Column(Text)
	content_html = Column(Text)

	def get_url(self):
		return '/article/%s' % self.url_key

class Page(Base):
	__tablename__ = 'pages'
	id = Column(Integer, primary_key=True)

	datetime_added = Column(DateTime, nullable=True,
							default=datetime.datetime.now)
	datetime_edited = Column(DateTime, nullable=True)

	name = Column(String(100)) # tag itself, eg. Science Olympiad
	url_key = Column(String(100)) # urlsafe, eg. science_olympiad

	content_mkdown = Column(Text)
	content_html = Column(Text)

	def get_url(self):
		return '/page/%s' % self.url_key

class Tag(Base):
	__tablename__ = 'tags'
	id = Column(Integer, primary_key=True)

	datetime_added = Column(DateTime, nullable=True,
							default=datetime.datetime.now)

	name = Column(String(100)) # tag itself, eg. Science Olympiad
	url_key = Column(String(100)) # urlsafe, eg. science_olympiad

	def get_url(self):
		return '/tag/%s' % self.url_key

# TODO
#class File(Base):
#	pass

"""
class Location(Base):
	__tablename__ = 'locations'
	id = Column(Integer, primary_key=True)

	datetime_added = Column(DateTime, nullable=True,
							default=datetime.datetime.now)

	position_x = Column(Float(255))
	position_y = Column(Float(255))

	name = Column(String(512))
	email = Column(String(512))
	phone = Column(String(512))
	school = Column(String(512)) # school/district

	def get_name(self):
		#title = 'Untitled' if not self.title else self.title
		#return 'Chat %d: %s' % (self.id, title)
		pass

	def get_url(self):
		#return '/chat/view/%d' % self.id
		pass

	def to_json(self):
		#return json.dumps({
		#	'title': self.title,
		#	'issue': self.issue,
		#	'users': None
		#})
		pass

	def serialize(self):
		return {
			'id': self.id,
			'position': {
				'x': self.position_x,
				'y': self.position_y,
			},
		}

class LocationForm(Form):
    position_x = TextField('x',
			[validators.Length(min=0, max=7)])

    position_y = TextField('y',
			[validators.Length(min=0, max=7)])

    name = TextField('Name',
			[validators.Length(min=2, max=255)])

    email = TextField('Email Address',
			[validators.Length(min=4, max=95)])

    phone = TextField('Phone',
			[validators.Length(min=4, max=20)])

    school = TextField('School/Institution',
			[validators.Length(min=4, max=255)])

"""