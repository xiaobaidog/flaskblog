from datetime import datetime

from exts import db


class Article(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(50), nullable=False)
  content = db.Column(db.Text, nullable=False)
  pdatetime = db.Column(db.DateTime, default=datetime.now)
  click_num = db.Column(db.Integer, default=0)
  save_num = db.Column(db.Integer, default=0)
  love_num = db.Column(db.Integer, default=0)
  #  外键 同步到数据库的外键关系
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)
  comments = db.relationship('Comment', backref='article')

  def __str__(self):
    return self.title


class Comment(db.Model):
  #  自定义表名
  __tablename__ = 'comment'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  comment = db.Column(db.String(300), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
  cdatetime = db.Column(db.DateTime, default=datetime.now)

  def __str__(self):
    return self.comment


class Article_type(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  type_name = db.Column(db.String(20), nullable=False)
  articles = db.relationship('Article', backref='article_type')
