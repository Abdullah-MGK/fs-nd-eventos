import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import exc
import json
#from decouple import config

db = SQLAlchemy()

# binds a flask application and a SQLAlchemy service
def setup_db(app, database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)

def db_create_all():
  db.create_all()

def db_drop_and_create_all():
  db.drop_all()
  db.create_all()


## Models

# Event
class Event(db.Model):
  __tablename__ = 'events'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  genre = db.Column(db.ARRAY(db.String))
  province = db.Column(db.String(120))
  city = db.Column(db.String(120))
  date = db.Column(db.DateTime)
  image_link = db.Column(db.String(500))
  manager_id = db.Column(db.Integer, db.ForeignKey('managers.id', ondelete="CASCADE"))
  event_attendance = db.relationship('EventAttendance', backref='event', lazy=True, cascade="all, delete-orphan")
  
  def __repr__(self):
    return json.dumps(self.format())

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'genre':  self.genre,
      'province': self.province,
      'city': self.city,
      'date': self.date,
      'image_link': self.image_link,
      'manager_id': self.manager_id
    }
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()


# Manager
class Manager(db.Model):
  __tablename__ = 'managers'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  events = db.relationship('Event', backref='manager', lazy=True, cascade="all, delete-orphan")
  
  def __repr__(self):
    return json.dumps(self.format())
  
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'phone': self.phone,
      'website': self.website,
      'image_link': self.image_link
    }
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()


# Participant
class Participant(db.Model):
  __tablename__ = 'participants'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  phone = db.Column(db.String(120))
  event_attendance = db.relationship('EventAttendance', backref='participant', lazy=True, cascade="all, delete-orphan")
  
  def __repr__(self):
    return json.dumps(self.format())
  
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'phone': self.phone
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()


class EventAttendance(db.Model):
  __tablename__ = 'event_attendance'
  
  id = db.Column(db.Integer, primary_key=True)
  checked_in = db.Column(db.Boolean, default=False)
  event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
  participant_id = db.Column(db.Integer, db.ForeignKey('participants.id', ondelete="CASCADE"), nullable=False)
  
  def __repr__(self):
    return json.dumps(self.format())
  
  def format(self):
    return {
      'id': self.id,
      'checked_in': self.checked_in,
      'event_id': self.event_id,
      'participant_id': self.participant_id
    }
