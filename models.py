import os
from sqlalchemy import Column, String, Integer, create_engine, JSON
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
#from flask import Flask


#database_name = "games"
#database_path = 'postgres://fwkpnotv:1wvhldt6f766_VfD2ighEipij_Q9xQJL@rogue.db.elephantsql.com:5432/fwkpnotv'
# FOR REPL
#database_path = 'postgres://fwkpnotv:1wvhldt6f766_VfD2ighEipij_Q9xQJL@rogue.db.elephantsql.com:5432/fwkpnotv'
# FOR HOME POSTGRES
database_path = 'postgresql://postgres_user:9Krokodilai@localhost:5432/games'


#app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fwkpnotv:1wvhldt6f766_VfD2ighEipij_Q9xQJL@rogue.db.elephantsql.com:5432/fwkpnotv'



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
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)
'''
class State(db.Model):
  __tablename__ = 'states'
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer, db.ForeignKey('game.id',  onupdate="CASCADE", ondelete="CASCADE"))
  games = db.relationship('Game', backref=db.backref('state', lazy=True))
  move_number = db.Column(db.Integer, nullable=False)
  move = db.Column(db.String(20), nullable=False)
  position = db.Column(db.JSON, nullable=False)

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'game_id': self.game_id,
      'move_number': self.move_number,
      'position': self.position,
      #'game': self.games,
      'move': self.move
    }


class Game(db.Model):
  __teblename__ = 'games'
  id = db.Column(db.Integer, primary_key=True)
  player_one = db.Column(db.Integer, db.ForeignKey('players.id',  onupdate="CASCADE", ondelete="CASCADE"))
  player_two = db.Column(db.Integer, db.ForeignKey('players.id',  onupdate="CASCADE", ondelete="CASCADE"))
  player = db.relationship('Player', foreign_keys=[player_one],  backref=db.backref('game', lazy=True))
  oponent = db.relationship('Player', foreign_keys=[player_two], backref=db.backref('game_against', lazy=True))
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'playerOne': self.player_one,
      'playerTwo': self.player_two
    }

class Offer(db.Model):
  __teblename__ = 'offers'
  id = db.Column(db.Integer, primary_key=True)
  player_one = db.Column(db.Integer, db.ForeignKey('players.id',  onupdate="CASCADE", ondelete="CASCADE"))
  player = db.relationship('Player', foreign_keys=[player_one],  backref=db.backref('offer', lazy=True))

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'playerOne': self.player_one
    }

class Player(db.Model):  
  __tablename__ = 'players'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), nullable=False, default='Guest')
  email = db.Column(db.String(50), nullable=False, default='Guest')
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  rating = db.Column(db.Integer, nullable=False, default='100')

  # def __init__(self, name, email, rating):
  #   self.name = name
  #   self.email = email
  #   self.rating = rating

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email,
      'date': self.date,
      'rating': self.rating
    }

'''
Category

'''
'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }
'''