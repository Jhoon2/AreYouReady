from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:testdb@cluster0.ej5hjgf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/supplies", methods=["POST"])
def supplies_post():
    supplies_receive = request.form['supplies_give']
    supplies_list = list(db.supplies.find({}, {'_id': False}))
    count = len(supplies_list) + 1

    doc = {
        'num': count,
        'supplies': supplies_receive,
        'done': 0,
        'comment': ''
    }

    db.supplies.insert_one(doc)

    return jsonify({'msg': '등록 완료!', 'supplies': supplies_list, 'count': count})

@app.route("/supplies/done", methods=["POST"])
def supplies_done():
    num_receive = request.form['num_give']
    supplies_num = db.supplies.find_one({'num': int(num_receive)})
    print(supplies_num['done'])
    if supplies_num['done'] == 0:
        db.supplies.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    else:
        db.supplies.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '체크 완료!', 'done': supplies_num['done']})

@app.route("/supplies/delete", methods=["POST"])
def supplies_delete():
    num_receive = request.form['num_give']
    db.supplies.delete_one({'num': int(num_receive)})
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
    app.run('0.0.0.0', port=3000, debug=True)
