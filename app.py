from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:testdb@cluster0.ej5hjgf.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/travel", methods=["POST"])
def travel_write():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    travel_list = list(db.travels.find({}, {'_id': False}))
    count = len(travel_list) + 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # title = soup.select_one('meta[name="twitter:title"]')['content']
    # image = soup.select_one('meta[name="twitter:image"]')['content']
    # desc = soup.select_one('meta[name="twitter:description"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'num': count,
        'title': title,
        'image': image,
        'desc': desc,
        'comment': comment_receive,
        'supplieslist': []
    }
    db.travels.insert_one(doc)
    return jsonify({'msg': '저장완료'})

@app.route("/travel", methods=["GET"])
def travel_read():
    travel_list = list(db.travels.find({},{'_id':False}))
    return jsonify({'travels': travel_list})

@app.route("/supplies", methods=["POST"])
def supplies_write():
    supplies_receive = request.form['supplies_give']
    num_receive = request.form['num_give']
    travel_list = db.travels.find_one({'num': int(num_receive)})
    count = len(travel_list['supplieslist']) + 1

    doc = {
        'index': count,
        'supplies': supplies_receive,
        'done': 0,
        'comment': ''
    }

    db.travels.update_one({'num': int(num_receive)}, {'$addToSet': {'supplieslist': doc}})
    return jsonify({'msg': '준비물 저장 완료!'})

@app.route("/travel/supplies", methods=["POST"])
def supplies_read():
    num_receive = request.form['num_give']
    travel_list = db.travels.find_one({'num': int(num_receive)})
    return jsonify({'msg': '완료!!', 'supplieslist': travel_list['supplieslist']})

@app.route("/supplies/done", methods=["POST"])
def supplies_done():
    index_receive = request.form['index_give']
    num_receive = request.form['currentNum_give']

    travel_list = db.travels.find_one({'num': int(num_receive)})

    update_num = travel_list['supplieslist'][int(index_receive) - 1]
    index = list(update_num.keys())[0]
    done = list(update_num.keys())[2]
    print(index)
    print(done)
    print(update_num)
    print(index_receive)

    if (update_num['done'] == 0):
        doc = {
            'index': int(index_receive),
            'supplies': '',
            'done': 1,
            'comment': ''
        }
    else:
        doc = {
            'index': int(index_receive),
            'supplies': '',
            'done': 0,
            'comment': ''
        }

    if update_num['done'] == 0:
        print('hahahahah')
        db.travels.update_one({'num': int(num_receive)}, {'$addToSet': {'supplieslist': doc}})
    else:
        print('hohohoho')
        db.travels.update_one({'num': int(num_receive)}, {'$addToSet': {'supplieslist': doc}})
    return jsonify({'msg': '체크 완료!'})
    # return jsonify({'msg': '체크 완료!', 'done': supplies_num['done']})

@app.route("/supplies/delete", methods=["POST"])
def supplies_delete():
    index_receive = request.form['index_give']
    currentnum_receive = request.form['currentnum_give']
    print(index_receive, currentnum_receive)
    # db.supplies.delete_one({'num': int(index_receive)})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/supplies/all_delete", methods=["POST"])
def delete_all():
    db.supplies.delete_many({})
    return jsonify({'msg': '전체 삭제 완료!'})

@app.route("/supplies", methods=["GET"])
def supplies_get():
    supplies_list = list(db.supplies.find({}, {'_id': False}))
    return jsonify({'supplies': supplies_list})

@app.route("/supplies/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    num_receive = request.form['num_give']
    supplies_num = db.supplies.find_one({'num': int(num_receive)})
    print(supplies_num)
    db.supplies.update_one({'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    supplies_list = list(db.supplies.find({}, {'_id': False}))
    return jsonify({'msg': '등록 완료!', 'supplies': supplies_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=3001, debug=True)
