from flask import Blueprint, render_template, request

from apps.goods.models import Goods, User_goods
from apps.user.models import User
from exts import db

good_bp = Blueprint('goods', __name__)


@good_bp.route('/findgoods')
def find_goods():
  uid = request.args.get('uid')
  user = User.query.get(uid)
  return render_template('goods/findgoods.html', user=user)


@good_bp.route('/foodusers')
def find_users():
  gid = request.args.get('gid')
  goods = Goods.query.get(gid)
  return render_template('goods/finduser.html', goods=goods)


@good_bp.route('/show')
def goods_show():
  users = User.query.filter(User.isdelete == False).all()
  goods = Goods.query.all()
  return render_template('goods/show.html', users=users, goods=goods)


@good_bp.route('/buy')
def buy():
  uid = request.args.get('uid')
  gid = request.args.get('gid')
  user_goods = User_goods()
  user_goods.user_id = uid
  user_goods.goods_id = gid
  db.session.add(user_goods)
  db.session.commit()
  return 'success'
