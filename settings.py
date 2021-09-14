import os


class Config:
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flaskblog2'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = True
  SECRET_KEY = 'jcm123asd'

  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

  STATIC_DIR = os.path.join(BASE_DIR, 'static')
  TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
  UPLOAD_DIR = os.path.join(STATIC_DIR, 'upload')
  UPLOAD_ICON_DIR = os.path.join(UPLOAD_DIR, 'icon')
  UPLOAD_PHOTO_DIR = os.path.join(UPLOAD_DIR, 'photo')


class DevelopmentConfig(Config):
  ENV = 'development'


class ProductionConfig(Config):
  ENV = 'production'
  DEBUG = False


