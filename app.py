from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@Cluster0.j0ygw.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('1PAGE.html')

@app.route('/2PAGE')
def page_1():
    return render_template('2PAGE.html')

@app.route('/1PAGE')
def page_2():
    return render_template('1PAGE.html')

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

@app.route("/travel/delete", methods=["POST"])
def travel_delete():
    num_receive = request.form['num_give']

    db.travels.delete_one({'num': int(num_receive)})

    all_list = list(db.travels.find({},{'_id':False}))
    
    reset_num = len(all_list)

# all_list[x]['num'] = x + 1
    
    if reset_num > 1:
        for x in range(int(num_receive), reset_num + 1):
            a = x + 1
            db.travels.update_one({'num': int(a)}, {'$set': {'num': x}})
    elif reset_num == 1:
        lastnum = 2
        db.travels.update_one({'num': int(lastnum)}, {'$set': {'num': 1}})
    
    
    #travel collection안에 length가 1보다 클경우는 num값을 length에 맞춰서 순차적으로 지정해주었습니다. 이유는 하나만 남겼을때는 num값을 1로 지정해줄수가 없고 2로 남아있는데
    #length가 1일경우에는 num값이 2인곳을 찾아 1로 바꾸어줘 최종적으로 하나 남았을때의 num값은 1입니다.
      

    return jsonify({'numdone': str(num_receive) + "삭제완료"})


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
    return jsonify({'msg': '준비물 저장 완료!', 'num': int(num_receive), 'index': count})


@app.route("/travel/supplies", methods=["POST"])
def supplies_read():
    num_receive = request.form['num_give']
    travel_list = db.travels.find_one({'num': int(num_receive)})
    return jsonify({'msg': '완료!!', 'modal-title': travel_list['comment'], 'supplieslist': travel_list['supplieslist']})



@app.route("/supplies/done", methods=["POST"])
def supplies_done():
    index_receive = request.form['index_give']
    num_receive = request.form['currentNum_give']

    travel_list = db.travels.find_one({'num': int(num_receive)})

    if travel_list['supplieslist'][int(index_receive) - 1]['done'] == 0:
        db.travels.update_one({"$and": [{'num': int(num_receive)}, {'supplieslist.index': int(index_receive)}]}, {'$set': {'supplieslist.$.done': 1}})
    else:
        db.travels.update_one({"$and": [{'num': int(num_receive)}, {'supplieslist.index': int(index_receive)}]}, {'$set': {'supplieslist.$.done': 0}})
    return jsonify({'msg': '체크 완료!', 'supplieslist': travel_list['supplieslist']})
    # return jsonify({'msg': '체크 완료!', 'done': supplies_num['done']})



@app.route("/supplies/delete", methods=["POST"])
def supplies_delete():
    index_receive = request.form['index_give']
    num_receive = request.form['currentNum_give']
    db.travels.update_one({'num': int(num_receive)}, {'$pull': {'supplieslist': {'index': int(index_receive)}}})

    travel_list = db.travels.find_one({'num': int(num_receive)})
    print(travel_list['supplieslist'])
    reset_num = len(travel_list['supplieslist'])

    for x in range(reset_num):
        travel_list['supplieslist'][x]['index'] = (x + 1)

    db.travels.update_one({'num': int(num_receive)}, {'$set': {'supplieslist': []}})
    db.travels.update_one({'num': int(num_receive)}, {'$addToSet': {'supplieslist': {'$each': travel_list['supplieslist']}}})
    return jsonify({'msg': '삭제 완료!'})



@app.route("/supplies/all_delete", methods=["POST"])
def delete_all():
    num_receive = request.form['currentNum_give']

    db.travels.update_one({'num': int(num_receive)}, {'$set': {'supplieslist': []}})
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



