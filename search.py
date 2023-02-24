import pymysql
import jwt
import requests
from flask import Blueprint, request, send_from_directory, jsonify
from flask_httpauth import HTTPBasicAuth
import manage
dbUser = 'root'
dbPassword = '123456'
db = pymysql.connect(host='localhost', user=dbUser, password=dbPassword, database='PYTHON')
c = db.cursor()
auth = HTTPBasicAuth()
SKEY = "123456"
algo = 'HS256'
lists=[]
ur = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_ga=GA1.2.1348005443.1674289286; _gid=GA1.2.38381321.1676887420; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1676288829,1676887420,1676899130; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1676899130; _gat=1; kw_token=XACP5IH6KW',
    'csrf': 'XACP5IH6KW',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn'
}
search = Blueprint('search', __name__)


@search.route('/search', methods=['GET'])
def search_kwd():
    try:
        token = request.headers['Authorization']
        jwt.decode(token, '123456', audience=manage.nowuser, algorithms=['HS256'])
    except:
        return jsonify(code=403, message='无法检验token，请尝试重新登陆')
    txts = request.query_string
    txt = str(txts).strip("b")
    txt = txt.strip("'")
    txt = txt.strip("text=")
    relists = search_keyword(txt)
    if type(relists) == type(0):
        return jsonify(code=403,message="没有找到任何结果呢，换个关键词试试吧！")
    return jsonify(code=200, message='success', data={'list': relists})


@search.route('/search/download/<int:rid>', methods=['GET'])
def download(rid):
    try:
        token = request.headers['Authorization']
        jwt.decode(token, '123456', audience=manage.nowuser, algorithms=['HS256'])
    except:
        return jsonify(code=403, message='无法检验token，请尝试重新登陆')
    url = 'https://link.hhtjim.com/kw/' + str(
        rid) + '.mp3'
    for i in range(0,10):
        if lists[i]['rid'] == rid:
            db.commit()
            c.execute("INSERT INTO python."+manage.nowuser+" (name, artist, album, duration, fav, rid) VALUES ('"+lists[i]['name']+"', '"+lists[i]['artist']+"', '"+lists[i]['album']+"', '"+lists[i]['duration']+"', 0, "+str(lists[i]['rid'])+")")
            db.commit()
    with open('temp.mp3', 'wb') as wstream:
        wstream.write(requests.get(url).content)
    try:
        return send_from_directory('', 'temp.mp3')
    except Exception as e:
        return jsonify(code=200, msg=str(e))


def search_keyword(keyword):
    global lists
    url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=' + keyword + '&pn=1&rn=10&httpsStatus=1&reqId' \
                                                                                    '=238306a0-b121-11ed-ae6d-f3575522368c'
    x = requests.get(url, headers=ur).json()
    first_lists = x['data']['list']
    if len(first_lists) == 0:
        return 10086
    artist_list = []
    rid_list = []
    album_list = []
    name_list = []
    length_list = []
    for i in range(0, 10):
        artist_list.append(first_lists[i]['artist'])
        rid_list.append(first_lists[i]['rid'])
        album_list.append(first_lists[i]['album'])
        name_list.append(first_lists[i]['name'])
        length_list.append(first_lists[i]['songTimeMinutes'])
    lists = []
    for i in range(0, 10):
        dict = {
            "name": name_list[i],
            "artist": artist_list[i],
            "album": album_list[i],
            "duration": length_list[i],
            "rid": rid_list[i]
        }
        lists.append(dict)
    return lists

