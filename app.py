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
secret = os.environ['SECRET']
auth_key = os.environ['AUTH0']
port = int(os.environ.get('PORT', 33507))
CORS(app)
def auth_required(f):

    def wrap(request, *args, **kwargs):
        auth = request.META.get('HTTP_AUTHORIZATION', None)

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
            payload = jwt.decode(
                token,
                auth_key
            )
        except jwt.ExpiredSignature:
            abort(404)
        except jwt.DecodeError:
            abort(404)


        return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__

    return wrap

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(data=models.Version.query.order_by('version desc').first().serialize)

@app.route('/', methods=['GET'])
def scores():
    return jsonify(data=[i.serialize for i in models.Scores.query.order_by('score desc').all()])

@app.route('/', methods=['POST'])
@auth_required
def post_scores():
    db.session.add(models.Scores(score_obj['name'], score_obj['score']))
    db.session.commit()
    return jsonify(data=[i.serialize for i in models.Scores.query.order_by('score desc').all()])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)
