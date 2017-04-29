#dependencies
import os
from boto.s3.connection import S3Connection
from flask import Flask, jsonify, request, abort
import json
from flask_sqlalchemy import SQLAlchemy
s3 = S3Connection(os.environ['DATABASE_URL'], os.environ['SECRET'])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
import models
secret = os.environ['SECRET']
port = int(os.environ.get('PORT', 33507))

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(data=models.Version.query.orderby('version desc').first().serialize)

@app.route('/', methods=['GET'])
def scores():


    token = request.headers.get('iusdhfihaisfjhaof')
    if token == secret:
        return jsonify(data=[i.serialize for i in models.Scores.query.order_by('score desc').all()])
    else: abort(404)

@app.route('/', methods=['POST'])
def post_scores():
    token = request.headers.get('iusdhfihaisfjhaof')
    if token == secret:
        score_obj = json.loads(request.data)

        db.session.add(models.Scores(score_obj['name'], score_obj['score']))
        db.session.commit()
        return jsonify(data=[i.serialize for i in models.Scores.query.order_by('score desc').all()])
    else: abort(404)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)
