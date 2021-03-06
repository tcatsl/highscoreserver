#dependencies
from functools import wraps
import os
from flask_cors import CORS, cross_origin
import jwt
from boto.s3.connection import S3Connection
from flask import Flask, jsonify, request, abort, redirect, session
import json
from flask_sqlalchemy import SQLAlchemy

s3 = S3Connection(os.environ['DATABASE_URL'], os.environ['AUTH0'])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
import models
import users
secret = os.environ['SECRET']
auth_key = os.environ['AUTH0']
port = int(os.environ.get('PORT', 33507))
CORS(app)

def get_auth():
    auth = request.headers.get('Authorization')
    if not auth:
        abort(404)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        abort(404)
    elif len(parts) == 1:
        abort(404)
    elif len(parts) > 2:
        abort(404)
    token = parts[1]
    try:
        return jwt.decode(
            token,
            auth_key,
            audience='YsIZfSDkbOYRuIDFuH64NhRywmQpz1kJ'
        )
    except jwt.ExpiredSignature:
        abort(404)
    except jwt.DecodeError:
        abort(404)

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(data=models.Version.query.order_by('version desc').first().serialize)
# @app.route('/my_stats', methods=['GET'])
# def my_stats():
#     get_auth()
#     return jsonify(session.query(func.avg(Scores.filter(db.session.query(users.App_users).filter(users.App_users.email == the_payload['email'])).label('average'))
@app.route('/', methods=['GET'])
def scores():
    return jsonify(data=[i.serialize for i in models.Scores.query.distinct(models.Scores.name, models.Scores.score, models.Scores.difficulty, models.Scores.duration, models.Scores.kills).order_by('score desc').all()])

@app.route('/', methods=['POST'])
def post_scores():
    the_payload = get_auth()
    print(the_payload)
    score_obj = json.loads(request.data)
    db.session.add(models.Scores(db.session.query(users.App_users).filter(users.App_users.email == the_payload['email']).first().user_name, score_obj['score'], score_obj['kills'], score_obj['difficulty'], score_obj['duration']))
    db.session.commit()
    return ""

@app.route('/is_user', methods=['GET'])
def is_user():
    payload = get_auth()
    if (db.session.query(users.App_users).filter(users.App_users.email == payload['email']).count() > 0):
        return db.session.query(users.App_users).filter(users.App_users.email == payload['email']).first().user_name
    else:
        return ""

@app.route('/newuser', methods=['POST'])
def post_user():
    new_payload = get_auth()
    user_str = json.loads(request.data)
    if (users.App_users.query.filter(users.App_users.user_name == user_str['user_name']).count() > 0):
        return "Bad"
    else:
        db.session.add(users.App_users(user_str['user_name'], new_payload['email']))
        db.session.commit()
        return user_str['user_name']

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)
