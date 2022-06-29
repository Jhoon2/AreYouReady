from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@Cluster0.j0ygw.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():


    return render_template('index.html')


@app.route("/travel", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

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
        'title' :title,
        'image' :image,
        'desc' :desc,
        'comment' :comment_receive
    }
    db.travels.insert_one(doc)


    return jsonify({'msg': '저장완료'})


@app.route("/travel", methods=["GET"])
def movie_get():

    travel_list = list(db.travels.find({},{'_id':False}))


    return jsonify({'travels': travel_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@Cluster0.j0ygw.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():


    return render_template('index.html')


@app.route("/travel", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

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
        'title' :title,
        'image' :image,
        'desc' :desc,
        'comment' :comment_receive
    }
    db.travels.insert_one(doc)


    return jsonify({'msg': '저장완료'})


@app.route("/travel", methods=["GET"])
def movie_get():

    travel_list = list(db.travels.find({},{'_id':False}))


    return jsonify({'travels': travel_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
