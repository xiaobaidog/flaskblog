import random

from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config


def upload_qiniu(filestorge):
  access_key = '-5l7R7MkuW-czNok8nT-Xe50yQr7HQ23yfE7pC1d'
  secret_key = 'pZn2eSrQHpfgVKKEfFcjo7NYD84VdQVn0fjmvgN-'

  q = Auth(access_key, secret_key)

  bucket_name = 'jcmblog'
  filename = filestorge.filename
  suffix = filename.rsplit('.')[-1]
  ran = random.randint(1, 1000)
  name = filename.rsplit('.')[0] + '_' + str(ran)
  key = name + '.' + suffix
  print(key)

  token = q.upload_token(bucket_name, key, 3600)

  ret, info = put_data(token, key, filestorge.read())
  return info, info, key


def delete_qiniu(filename):
  access_key = '-5l7R7MkuW-czNok8nT-Xe50yQr7HQ23yfE7pC1d'
  secret_key = 'pZn2eSrQHpfgVKKEfFcjo7NYD84VdQVn0fjmvgN-'

  q = Auth(access_key, secret_key)

  # 初始化BucketManager
  bucket = BucketManager(q)

  bucket_name = 'jcmblog'

  key = filename

  ret, info = bucket.delete(bucket_name, key)

  return ret, info
