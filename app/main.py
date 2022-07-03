import os
import pymongo
from pymongo import MongoClient
import certifi
import random

certificate = certifi.where()

password = os.environ["MONGO_PASSWORD"]
url = "mongodb+srv://renitaKurian:"+ password +"@datacluster.ylfhthx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url, tlsCAFile = certificate)
#print(client.server_info())

mydb = client.Quotes # to access database quotes
collection = mydb.Random

noQ = 0
objects = collection.find()
for i in objects:
    noQ+=1

from flask import Flask
from flask import render_template, request, redirect, url_for
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    objects = collection.find()
    n = random.randint(0, noQ-1)
    q = objects[n]
    quote = q['quote']
    auth = q['author']
    lang = q['lang']
    translation = q['translation']
    if request.method == 'POST':
        return render_template("home.html", quote = quote, author= auth, lang = lang, translation = translation)
    return render_template("home.html", quote = quote, author= auth, lang = lang, translation = translation)

@app.route("/addQuote/", methods=['GET', 'POST'])
def addQuote():
    if request.method == 'POST':
        q = request.form.get('quote')
        a = request.form.get('author')
        l = request.form.get('lang')
        t = request.form.get('translation')
        if(q!="" and q!=" "):
            qd = {"quote":q, "lang": l, "author":a, "translation": t}
            x = collection.insert_one(qd)
            return redirect(url_for('.home'))

    return render_template("addQuote.html")