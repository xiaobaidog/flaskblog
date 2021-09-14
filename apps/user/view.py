import hashlib
import os

from flask import Blueprint, render_template, request, redirect, jsonify, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps.article.models import Article_type, Article
from apps.user.models import User, Photo, AboutMe, MessageBoard
from apps.user.sessend import SmsSendAPIDemo
from apps.utills.utill import upload_qiniu, delete_qiniu
from exts import db
from settings import Config

user_bp = Blueprint('user', __name__, url_prefix='/user')

required_login_list = ['/user/center', '/user/change', '/article/publish', '/user/upload_photo',
                       '/user/show_photo', '/user/delete_photo', '/article/add_comment',
                       '/user/aboutme', '/user/showabout']


@user_bp.before_app_first_request
def first_request1():
  print('before_app_first_request')


@user_bp.before_app_request
def before_request1():
  print('before_request1', request.path)
  if request.path in required_login_list:
    uid = session.get('uid')
    if not uid:
      return render_template('user/login.html')
    else:
      user = User.query.get(uid)
      g.user = user


@user_bp.after_app_request
def after_request1(response):
  response.set_cookie('a')
  return response


@user_bp.app_template_filter('cdecode')
def content_decode(content):
  content = content.decode('utf-8')
  return content


@user_bp.route('/')
def index():
  # uid = request.cookies.get('uid', None)
  uid = session.get('uid')
  page_num = int(request.args.get('page', 1))
  pagination = Article.query.order_by(-Article.pdatetime).paginate(page=page_num, per_page=3)
  # pagination.items
  # pagination.page 当前页码数
  # pagination.prev_num 当前页码数的前一页
  # pagination.next_num 当前页码数的后一页
  # pagination.has_next    boolean
  # pagination.has_prev    boolean
  # pagination.pages    总页数
  # pagination.total    总的记录条数
  if uid:
    user = User.query.get(int(uid))
    return render_template('user/index.html', user=user, pagination=pagination)
  else:
    return render_template('user/index.html', pagination=pagination)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    repassword = request.form.get('repassword')
    phone = request.form.get('phone')
    email = request.form.get('email')
    if password == repassword:
      # 结合模型
      user = User()
      user.username = username
      user.password = generate_password_hash(password)
      user.phone = phone
      user.email = email
      # 添加
      db.session.add(user)
      db.session.commit()
      return redirect('/user')
  return render_template('user/register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    f = request.args.get('f')
    if f == '1':
      username = request.form.get('username')
      password = request.form.get('password')
      users_list = User.query.filter(User.username == username).all()
      for user in users_list:
        flag = check_password_hash(user.password, password)
        if flag:
          #  cookie
          #  response = redirect(url_for('user.index'))
          # response.set_cookie('uid', str(user.id), max_age=1800)
          # return response
          #  session
          session['uid'] = user.id
          return redirect(url_for('user.index'))
        else:
          return render_template('user/login.html', msg='用户名或者密码错误')

    elif f == '2':
      phone = request.form.get('phone')
      code = request.form.get('code')
      valid_code = session.get(phone)
      if code == valid_code:
        user = User.query.filter(User.phone == phone).first()
        if user:
          session['uid'] = user.id
          return redirect(url_for('user.index'))
        else:
          return render_template('user/login.html', msg='此号码没有注册！')
      else:
        return render_template('user/login.html', msg='验证码有误！')

  return render_template('user/login.html')


@user_bp.route('/sendMsg')
def send_message():
  phone = request.args.get('phone')
  SECRET_ID = "5e583417fffccfa0a9f0d5bc5d45c0b6"  # 产品密钥ID，产品标识
  SECRET_KEY = "c64b167e25197862f5312fcadc0d3f19"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
  BUSINESS_ID = "76cb306f7fa8437aa1f01853dba5ce21"  # 业务ID，易盾根据产品业务特点分配
  api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
  params = {
    "mobile": phone,
    "templateId": "10084",
    "paramType": "json",
    "params": "json格式字符串"
  }
  ret = api.send(params)
  print(ret)
  if ret is not None:
    if ret["code"] == 200:
      taskId = ret["data"]["taskId"]
      print("taskId = %s" % taskId)
      session[phone] = taskId
      return jsonify(code=200, msg='短信发送成功')
    else:
      print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
      return jsonify(code=400, msg='短信发送失败')
  return '1'


@user_bp.route('/checkPhone', methods=['GET', 'POST'])
def check_phone():
  phone = request.args.get('phone')
  user = User.query.filter(User.phone == phone).all()
  # code: 400 不能用  200 可以用
  if len(user) > 0:
    return jsonify(code=400, msg='此号码已被注册')
  else:
    return jsonify(code=200, msg='此号码可用')


@user_bp.route('/logout')
def logout():
  # response = redirect(url_for('user.index'))
  # response.delete_cookie('uid')

  # del session['uid']

  session.clear()
  return redirect(url_for('user.index'))


@user_bp.route('/center')
def user_center():
  types = Article_type.query.all()
  photos = Photo.query.filter(Photo.user_id == g.user.id).all()
  return render_template('user/center.html', user=g.user, types=types, photos=photos)


ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp', 'avi']


@user_bp.route('/change', methods=['GET', 'POST'])
def user_change():
  if request.method == 'POST':
    username = request.form.get('username')
    print('++++++++++', username)
    phone = request.form.get('phone')
    email = request.form.get('email')
    icon = request.files.get('icon')
    icon_name = icon.filename
    suffix = icon_name.rsplit('.')[-1]
    print('========', suffix)
    if suffix in ALLOWED_EXTENSIONS:
      icon_name = secure_filename(icon_name)  # 保证文件名字符合python命名规则
      file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
      print('_______', file_path)
      icon.save(file_path)
      user = g.user
      user.username = username
      user.phone = phone
      user.email = email
      path = 'upload/icon/' + icon_name
      user.icon = path
      db.session.commit()
      return redirect(url_for('user.user_center'))
    else:
      return render_template('user/center.html', user=g.user, msg='图片格式错误')
  return render_template('user/center.html', user=g.user)


@user_bp.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
  photo = request.files.get('photo')
  ret, info, filename = upload_qiniu(photo)
  print(info)
  print()
  if info.status_code == 200:
    photo = Photo()
    photo.photo_name = filename
    photo.user_id = g.user.id
    db.session.add(photo)
    db.session.commit()
    return 'success'
  else:
    return '失败'


@user_bp.route('/show_photo')
def show_photo():
  photos = Photo.query.filter(Photo.user_id == g.user.id).all()
  return render_template('user/show_photo.html', photos=photos, user=g.user)


@user_bp.route('/delete_photo')
def delete_photo():
  pid = request.args.get('pid')
  photo = Photo.query.get(pid)
  filename = photo.photo_name
  ret, info = delete_qiniu(filename)
  if info.status_code == 200:
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('user.user_center'))
  else:
    referer = request.headers.get('Referer', None)
    return render_template('500.html', msg='删除失败', referer=referer)


@user_bp.route('/aboutme', methods=['GET', 'POST'])
def about_me():
  content = request.form.get('about')
  try:
    aboutme = AboutMe()
    aboutme.content = content.encode('utf-8')
    aboutme.user_id = g.user.id
    db.session.add(aboutme)
    db.session.commit()
  except Exception as err:
    return redirect(url_for('user.user_center'))
  else:
    return render_template('user/aboutme.html', user=g.user)


@user_bp.route('/showabout')
def show_about():
  return render_template('user/aboutme.html', user=g.user)


@user_bp.route('/board', methods=['GET', 'POST'])
def show_board():
  page = int(request.args.get('page', 1))
  # boards = MessageBoard.query.filter().paginate(page=page, per_page=5)
  boards = MessageBoard.query.paginate(page=page, per_page=5)
  uid = session.get('uid', None)
  user = None
  if uid:
    user = User.query.get(uid)

  if request.method == 'POST':
    content = request.form.get('board')
    msg_board = MessageBoard()
    msg_board.content = content
    if uid:
      msg_board.user_id = uid
    db.session.add(msg_board)
    db.session.commit()
    return redirect(url_for('user.show_board'))

  return render_template('user/board.html', user=user, boards=boards)


@user_bp.route('/board_delete')
def board_delete():
  bid = request.args.get('bid')
  if bid:
    message = MessageBoard.query.get(bid)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('user.user_center'))


