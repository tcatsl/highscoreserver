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

@app.route('/', methods=['GET'])
def scores():
    return jsonify(data=[i.serialize for i in models.Scores.query.order_by('score desc').all()])

@app.route('/', methods=['POST'])
def post_scores():
    the_payload = get_auth()
    print(the_payload)
    score_obj = json.loads(request.data)
    db.session.add(models.Scores(score_obj['name'], score_obj['score']))
    db.session.commit()
    return jsonify(data=[i.serialize for i in models.Scores.query.order_by('score desc').all()])
@app.route('/user', methods=['POST'])
def post_user():
    the_payload = get_auth()
    user_obj = json.loads(request.data)
    db.session.add(users.Users(user_obj['user_name'], the_payload['email']))
    db.session.commit()
    return 201

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)
