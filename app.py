from curses import meta
from operator import index, indexOf
from turtle import pos

import pymysql
import sqlalchemy

from flask import Flask, request, render_template, redirect, session, url_for, send_file, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_cors import CORS
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from uuid import uuid4

import io
import os
import traceback
import random
import base64
import json
import re

app=Flask(__name__)
app.debug = False
cors = CORS(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = {
    'user' : 'root'
    , 'password' : 'rhaehfl0123'
    , 'host' : 'localhost'
    , 'port' : 3306
    , 'database' : 'snowman'
}
DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
sqlAdd = ""

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'FDS1657124JFDS&876$$*@$@~!!!dfdfa12FDDFDD'

engine = create_engine(DB_URL, encoding='utf-8')
conn = engine.connect()

db = SQLAlchemy(app)

#app.databse = database

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class EachSnowman(db.Model):
    __tablename__ = 'each_snowman'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(10), nullable=False)   
    hit_count = db.Column(db.Integer, nullable=False)   
    head_accessary = db.Column(db.Integer, nullable=False)   
    body_accessary = db.Column(db.Integer, nullable=False)   
    eye = db.Column(db.Integer, nullable=False)   
    nose = db.Column(db.Integer, nullable=False)   
    mouth = db.Column(db.Integer, nullable=False)   
    arms = db.Column(db.Integer, nullable=False)   
    wreath_accessary = db.Column(db.Integer, nullable=False)   
    createdAt = db.Column(db.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))    

class Message(db.Model):
    __tablename__ = 'message'

    snowman_id = db.Column(db.ForeignKey('each_snowman.id', ondelete='CASCADE'), primary_key=True)
    nickname = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(100), nullable=False)   
    interaction = db.Column(TINYINT, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))    

@app.route('/')
def main_page():
    return render_template('snowman.html')

@app.route('/make_snowman', methods = ["POST"])
def make_snowman():
    json_data = request.get_json()
    nickname = json_data["nickname"]
    head_accessary = json_data["head_accessary"]
    body_accessary = json_data["body_accessary"]
    eye = json_data["eye"]
    nose = json_data["nose"]
    mouth = json_data["mouth"]
    arms = json_data["arms"]
    wreath_accessary = json_data["wreath_accessary"]

    snowman = EachSnowman(nickname=nickname, hit_count=0, head_accessary=head_accessary, body_accessary=body_accessary, eye=eye, nose=nose, mouth=mouth, arms=arms, wreath_accessary=wreath_accessary)
    db.session.add(snowman)
    db.session.commit()
    
    returnUrl = "/show?nickname=" + nickname
    return redirect(returnUrl)


@app.route('/make_page')
def make_page():
    return render_template('make_snowman.html')

@app.route('/show', methods=["GET"])
def show():
    nickname = request.args.get("nickname", type=str)
    snowman = EachSnowman.query.filter_by(nickname=nickname).first()
    #return render_template('snowman.html')
    return render_template('snowman.html', nickname= nickname,hit_count=snowman.hit_count, head_accessary=snowman.head_accessary, body_accessary=snowman.body_accessary, eye=snowman.eye, nose=snowman.nose, mouth=snowman.mouth, arms=snowman.arms, wreath_accessary=snowman.wreath_accessary )

@app.route('/help', methods=["POST"])
def help():
    json_data = request.get_json()
    nickname = json_data["nickname"]
    snowman = EachSnowman.query.filter_by(nickname=nickname).first()
    if snowman.hit_count != 0:
        snowman.hit_count -= 1
    nickname_input = json_data["nickname_input"]
    message = json_data["message"]
    letter = Message(snowman_id = snowman.id, nickname = nickname_input, message=message, interaction=1)
    db.session.add(letter)
    db.session.commit()
    return "ok"


@app.route('/destroy', methods=["POST"])
def destroy():
    json_data = request.get_json()
    nickname = json_data["nickname"]
    snowman = EachSnowman.query.filter_by(nickname=nickname).first()
    if snowman.hit_count != 3:
        snowman.hit_count += 1
    nickname_input = json_data["nickname_input"]
    message = json_data["message"]
    letter = Message(snowman_id = snowman.id, nickname = nickname_input, message=message, interaction=1)
    db.session.add(letter)
    db.session.commit()
    return "ok"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
