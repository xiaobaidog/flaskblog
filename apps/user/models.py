from datetime import datetime

from exts import db


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(15), nullable=False)
  password = db.Column(db.String(200), nullable=False)
  phone = db.Column(db.String(11), unique=True, nullable=False)
  email = db.Column(db.String(30))
  icon = db.Column(db.String(100))
  isdelete = db.Column(db.Boolean, default=False)
  rdatatime = db.Column(db.DateTime, default=datetime.now)
  articles = db.relationship('Article', backref='user')
  comments = db.relationship('Comment', backref='user')

  def __str__(self):
    return self.username


class Photo(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  photo_name = db.Column(db.String(100), nullable=False)
  photo_datetime = db.Column(db.DateTime, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __str__(self):
    return self.photo_name


class AboutMe(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  content = db.Column(db.BLOB, nullable=False)
  pdatetime = db.Column(db.DateTime, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
  user = db.relationship('User', backref='aboutme')


class MessageBoard(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  content = db.Column(db.String(255), nullable=False)
  mdatetime = db.Column(db.DateTime, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  user = db.relationship('User', backref='messages')