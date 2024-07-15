from datetime import datetime

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo


def load_secret(name):
    return open('/run/secrets/%s' % name).read().strip()


def get_dsn(host, user, password, db):
    return 'mongodb://%s:%s@%s/%s?authSource=admin' % (
        load_secret(user), load_secret(password), host, db
    )


app = Flask(__name__)
app.config['MONGO_URI'] = get_dsn(
    'mongo',
    'mongo_root_username',
    'mongo_root_password',
    'test_database',
)
mongo = PyMongo(app)


@app.get('/')
def index():
    mongo.db.access_log.insert_one({
        'ip': request.remote_addr,
        'browser': request.headers['User-Agent'],
        'timestamp': datetime.utcnow(),
    })
    visits = mongo.db.access_log.aggregate([
        {
            '$match': {
                'ip': request.remote_addr,
            },
        },
        {
            '$group': {
                '_id': '$browser',
                'count': {'$sum': 1},
                'lastVisit': {'$max': '$timestamp'},
            },
        },
        {
            '$project': {
                '_id': 0,
                'browser': '$_id',
                'count': 1,
                'lastVisit': 1,
            },
        },
    ])
    return jsonify(list(visits))
