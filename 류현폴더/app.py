from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.xaxuh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/index')
def page_1():
    return render_template('index.html')


@app.route("/supplies", methods=["POST"])
def supplies_post():
    supplies_receive = request.form['supplies_give']
    num_receive = request.form['num_give']
    travel_list = db.travels.find_one({'num': int(num_receive)})
    count = len(travel_list['supplies']) + 1

    doc = {
        'index': count,
        'supplies': supplies_receive,
        'done': '0',
        'comment': ''
    }

    db.travels.update_one({'num': int(num_receive)}, {'$addToSet': {'supplies': doc}})
    return jsonify({'msg': '준비물 저장 완료!', 'num': count})



@app.route("/travel", methods=["POST"])
def travel_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    travel_list = list(db.travels.find({}, {'_id': False}))
    count = len(travel_list) + 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'num': count,
        'title': title,
        'image': image,
        'desc': desc,
        'comment': comment_receive,
        'supplies': []
    }
    db.travels.insert_one(doc)
    return jsonify({'msg': '저장완료'})




@app.route("/travel", methods=["GET"])
def travel_get():
    travel_list = list(db.travels.find({},{'_id':False}))
    return jsonify({'travels': travel_list})



@app.route("/travel/supplies", methods=["POST"])
def travel_supplies_read():
    num_receive = request.form['num_give']
    travel_list = db.travels.find_one({'num': int(num_receive)})
    return jsonify({'msg': 'OKOKOKOKOK', 'supplies': travel_list['supplies']})


@app.route("/supplies/done", methods=["POST"])
def supplies_done():
    index_receive = request.form['index_give']
    num_receive = request.form['currentNum_give']

    travel_list = db.travels.find_one({'num': int(num_receive)})
    print(travel_list)

    update_num = travel_list['supplies'][int(index_receive) - 1]
    print(update_num)

    if update_num['done'] == '0':
        db.travels.update_one({'num': int(num_receive)}, {'$addToset' : {update_num['supplies'] : 'aaaa'}})
        print(update_num['done'])

    # db.travels.update_one({'num': int(num_receive)}, {'$addToSet': {'supplies': 1}})
    return jsonify({'msg': '체크 완료!'})
    # return jsonify({'msg': '체크 완료!', 'done': supplies_num['done']})



if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)





