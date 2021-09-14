from flask import Blueprint, request, g, redirect, url_for, render_template, jsonify, session

from apps.article.models import Article, Article_type, Comment
from apps.user.models import User
from exts import db

article_bp1 = Blueprint('article', __name__, url_prefix='/article')


@article_bp1.route('/publish', methods=['GET', 'POST'])
def article_publish():
  if request.method == 'POST':
    title = request.form.get('title')
    type_id = request.form.get('type')
    content = request.form.get('content')
    article = Article()
    article.title = title
    article.type_id = type_id
    article.content = content
    article.user_id = g.user.id
    db.session.add(article)
    db.session.commit()
    return redirect(url_for('user.index'))
  return redirect(url_for('user.user_center'))


@article_bp1.route('/detail')
def article_detail():
  article_id = request.args.get('aid')
  article = Article.query.get(article_id)
  types = Article_type.query.all()
  user_id = session.get('uid')
  user = None
  if user_id:
    user = User.query.get(user_id)
  page = int(request.args.get('page', 1))
  comments = Comment.query.filter(Comment.article_id == article_id).paginate(page=page, per_page=5)
  return render_template('article/detail.html', article=article, types=types, user=user, comments=comments)


@article_bp1.route('love')
def article_love():
  article_id = request.args.get('aid')
  tag = request.args.get('tag')
  article = Article.query.get(article_id)
  if tag == '1':
    article.love_num -= 1
  else:
    article.love_num += 1
  db.session.commit()
  return jsonify(love=article.love_num)


@article_bp1.route('/add_comment', methods=['GET', "POST"])
def add_comment():
  if request.method == 'POST':
    comment = request.form.get('comment')
    user_id = g.user.id
    article_id = request.form.get('aid')
    comment1 = Comment()
    comment1.comment = comment
    comment1.user_id = user_id
    comment1.article_id = article_id
    db.session.add(comment1)
    db.session.commit()
    return redirect(url_for('article.article_detail') + "?aid=" + article_id)
  return redirect(url_for('user.index'))
