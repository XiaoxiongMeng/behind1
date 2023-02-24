import jwt
from flask import request, Blueprint, jsonify
import pymysql
import manage

dbUser = 'root'
dbPassword = '123456'
db = pymysql.connect(host='localhost', user=dbUser, password=dbPassword, database='PYTHON')
c = db.cursor()
history = Blueprint('history', __name__)


@history.route('/user/history/', methods=['GET', 'DELETE'])
def hist2():
    try:
        token = request.headers['Authorization']
        jwt.decode(token, '123456', audience=manage.nowuser, algorithms=['HS256'])
    except:
        return jsonify(code=403, message='无法检验token，请尝试重新登陆')
    if request.method == 'DELETE':
        cont = request.json
        if cont['type'] == 1:
            nums = len(cont['list'])
            for i  in range(0,nums):
                c.execute("DELETE FROM " + manage.nowuser + " WHERE id="+str(cont['list'][i])+";")
                db.commit()
        else:
            c.execute("DELETE FROM " + manage.nowuser + " WHERE id=" + str(cont['id'])+ ";")
            db.commit()
        return jsonify(code=200, msg="success")
    else:
        page = request.query_string
        txt = str(page).strip("b")
        txt = txt.strip("'")
        txt = txt.strip("page=")
        start = int(txt) - 1
        global dict
        total = c.execute("SELECT * FROM " + manage.nowuser)
        db.commit()
        times = int(total / 10 + 0.9)
        c.execute("SELECT * FROM " + manage.nowuser + " LIMIT " + str(start * 10) + ", 10;")  #
        db.commit()
        list = []
        lists = c.fetchall()
        for u in range(0, len(lists)):
            dict = {
                "name": lists[u][1],
                "artist": lists[u][2],
                "album": lists[u][3],
                "duration": lists[u][4],
                "rid": lists[u][6],
                "fav": lists[u][5],
                "id": lists[u][0]
            }
            list.append(dict)
        return jsonify(code=200, message="success", data={'list': list, 'count': times})


@history.route('/user/history/lc', methods=['PUT'])
def lc():
    try:
        token = request.headers['Authorization']
        jwt.decode(token, '123456', audience=manage.nowuser, algorithms=['HS256'])
    except:
        return jsonify(code=403, message='无法检验token，请尝试重新登陆')
    cont = request.json
    c.execute("UPDATE " + manage.nowuser + " SET fav="+str(cont['fav'])+" WHERE id=" + str(cont['id']) + ";")
    db.commit()
    c.execute("SELECT t.* FROM python."+manage.nowuser+" t WHERE id LIKE '" + str(cont['id']) + "';")
    db.commit()
    resp = c.fetchone()
    return jsonify(code=200, message='success', data={'name': resp[1], 'artist': resp[2], 'album': resp[3], 'duration': resp[4], 'rid': resp[6]})


@history.route('/user/history', methods=['GET'])
def hist(): # 可能是什么未知BUG，删掉这个路由就不能跑了，但是带着这个路由就可以跑
    try:
        token = request.headers['Authorization']
        jwt.decode(token, '123456', audience=manage.nowuser, algorithms=['HS256'])
    except:
        return jsonify(code=403, message='无法检验token，请尝试重新登陆')
    page = request.query_string
    txt = str(page).strip("b")
    txt = txt.strip("'")
    txt = txt.strip("page=")
    start = int(txt) - 1
    global dict
    total = c.execute("SELECT * FROM " + manage.nowuser)
    db.commit()
    times = int(total / 10 + 0.9)
    c.execute("SELECT * FROM " + manage.nowuser + " LIMIT " + str(start * 10) + ", 10;")  #
    db.commit()
    list = []
    lists = c.fetchall()
    for u in range(0, len(lists)):
        dict = {
                "name": lists[u][1],
                "artist": lists[u][2],
                "album": lists[u][3],
                "duration": lists[u][4],
                "rid": lists[u][6],
                "fav": lists[u][5],
                "id": lists[u][0]
        }
        list.append(dict)
    return jsonify(code=200, message="success", data={'list': list, 'count': times})
