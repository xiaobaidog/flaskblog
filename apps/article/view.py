from flask import Blueprint, render_template, request

from apps.article.models import Article
from apps.user.models import User
from exts import db
# 测试用，与项目无关

article_bp = Blueprint('article', __name__)


@article_bp.route('/publish', methods=['GET', 'POST'])
def publish_article():
  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')
    uid = request.form.get('uid')
    article = Article()
    article.title = title
    article.content = content
    article.user_id = uid
    db.session.add(article)
    db.session.commit()
    return 'success'
  else:
    users = User.query.filter(User.isdelete == False).all()
    return render_template('article/add_article.html', users=users)


@article_bp.route('/all')
def all_article():
  articles = Article.query.all()
  return render_template('article/all.html', articles=articles)


@article_bp.route('/all1')
def all1_article():
  uid = request.args.get('id')
  user = User.query.get(uid)
  return render_template('article/all1.html', user=user)
