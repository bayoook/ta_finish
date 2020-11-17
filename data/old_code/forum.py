from flask import Flask, Response, render_template, redirect, jsonify
from datetime import datetime as date
from datetime import timedelta, datetime
from multiprocessing.pool import ThreadPool
import json
from time import sleep
from statistics import stdev
from pymongo import MongoClient
import sys
from pprint import pprint
context = ('/root/certs/min4tozaki.me.crt', '/root/certs/min4tozaki.me.key')
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='/root/ta/staticweb', static_folder='/root/ta/staticweb', static_url_path='')
port = sys.argv[1]

@app.route('/')
def default_web():
    return render_template('index.html')

@app.route('/kordas')
def form_kordas():
    return redirect('https://docs.google.com/forms/d/e/1FAIpQLSfr3ljTWxXsDzens3vaZ4YUpSrM9Sm9rSnlzy8suNmqz4ovbQ/viewform?usp=sf_link')

@app.errorhandler(404)
def not_found(e):
    return redirect('https://min4tozaki.me/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True, ssl_context=context)

