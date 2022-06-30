from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.xaxuh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('1PAGE.html')

@app.route('/2PAGE')
def page_1():
    return render_template('2PAGE.html')

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

    if travel_list['supplieslist'][int(index_receive) - 1]['done'] == 0:
        db.travels.update_one({"$and": [{'num': int(num_receive)}, {'supplieslist.index': int(index_receive)}]}, {'$set': {'supplieslist.$.done': 1}})
    else:
        db.travels.update_one({"$and": [{'num': int(num_receive)}, {'supplieslist.index': int(index_receive)}]}, {'$set': {'supplieslist.$.done': 0}})
    return jsonify({'msg': '체크 완료!'})
    # return jsonify({'msg': '체크 완료!', 'done': supplies_num['done']})

@app.route("/supplies/delete", methods=["POST"])
def supplies_delete():
    index_receive = request.form['index_give']
    num_receive = request.form['currentnum_give']
    print(index_receive, num_receive)
    db.supplies.delete_one({ "$and": [{'num': int(num_receive)}, {'supplieslist.index': int(index_receive)}]})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/supplies/all_delete", methods=["POST"])
def delete_all():
    db.supplies.delete_many({})
    return jsonify({'msg': '전체 삭제 완료!'})

@app.route("/supplies/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    num_receive = request.form['num_give']
    supplies_num = db.supplies.find_one({'num': int(num_receive)})
    db.supplies.update_one({'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    supplies_list = list(db.supplies.find({}, {'_id': False}))
    return jsonify({'msg': '등록 완료!', 'supplies': supplies_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)



