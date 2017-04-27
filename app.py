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
@app.route('/', methods=['GET'])
def scores():
    token = request.headers.get('secret')
    if token == secret:
        return jsonify(data=[i.serialize for i in models.Scores.query.all().order_by('score desc')])
    else: abort(404)

@app.route('/', methods=['POST'])
def post_scores():
    token = request.headers.get('secret')
    if token == secret:
        score_obj = json.JSONDecoder(request.data)
        new_score = Scores(score_obj.name, score_obj.score)
        db.session.add(new_score)
        db.session.commit()
        return jsonify(data=[i.serialize for i in models.Scores.query.all().order_by('score desc')])
    else: abort(404)


if __name__ == '__main__':
    app.debug = True
    app.run()
