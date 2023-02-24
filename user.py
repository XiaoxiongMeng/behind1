from datetime import timedelta, datetime
from flask import request, jsonify, Blueprint
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

import manage

user = Blueprint('user', __name__)
dbUser = 'root'
dbPassword = '123456'
db = pymysql.connect(host='localhost', user=dbUser, password=dbPassword, database='PYTHON')
c = db.cursor()
SKEY = "123456"
algo = 'HS256'
@user.route('/user', methods=['POST'])
def register():
    cont = request.json
    username = cont['username']
    a = c.execute("SELECT t.* FROM python.userdata t WHERE username LIKE '" + username + "' LIMIT 1;")
    db.commit()
    if username == "" or cont['password'] == "":
        return jsonify(code=403, message="账号或密码内容不能为空")
    elif a != 0:
        return jsonify(code=403, message="该用户已存在，请尝试换个用户名.")
    password = cont['password']
    psw = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    uid = c.execute("SELECT * FROM userdata") + 1
    db.commit()
    c.execute("INSERT INTO python.userdata (username, password) VALUES ('" + username + "', '" + psw + "')")
    db.commit()
    c.execute("""create table if not exists python."""+username+"""
(
    id       int auto_increment,
    name     varchar(40) null,
    artist   varchar(40) null,
    album    varchar(40) null,
    duration varchar(6)  null,
    fav      int         null,
    rid      int         null,
    constraint test2_pk
        primary key (id)
);""")
    db.commit()
    return jsonify(code=200, message='success', data={'id': uid, 'username': username})


@user.route('/user/login', methods=['POST'])
def login():
    cont = request.json
    username = cont['username']
    password = cont['password']
    try:
        c.execute("select password from userdata where username = '" + username + "';")
        x = c.fetchone()[0]
    except:
        return jsonify(code=403, message='用户名不存在！')
    if check_password_hash(x, password):
        access_token_expires = timedelta(seconds=36000)
        expire = datetime.utcnow() + access_token_expires
        payload = {
            "sub": 'login success',
            "iss": 'root',
            "aud": username,
            "exp": expire
        }
        access_token = jwt.encode(payload, SKEY, algorithm=algo)
        manage.nowuser = username
        return jsonify(code=200, message='success', data={'username': username, 'id': 1, 'token': access_token})
    else:
        return jsonify(code=403, message='密码错误！')
