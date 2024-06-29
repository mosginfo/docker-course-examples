import contextlib

from flask import Flask, request
from flask_cors import CORS
from flask_uploader import init_uploader
from flask_uploader import Uploader
from flask_uploader.exceptions import UploadNotAllowed
from flask_uploader.storages import FileSystemStorage
from flask_uploader.validators import (
    Extension,
    FileRequired,
    FileSize,
)
from pymysql import IntegrityError

from .flask_mysql import PyMySQL


app = Flask(__name__)
app.config.from_prefixed_env()
CORS(app)
init_uploader(app)

db = PyMySQL(app)

photos_storage = FileSystemStorage(dest='photos')
photos_uploader = Uploader(
    'photos',
    photos_storage,
    validators=[
        FileRequired(),
        FileSize('10Mb'),
        Extension(Extension.IMAGES),
    ]
)


@app.get('/')
def index():
    cursor = db.execute('SELECT id, lookup, created FROM photo')
    return [
        {'url': photos_uploader.get_url(p['lookup']), **p}
        for p in cursor.fetchall()
    ]


@app.post('/')
def upload():
    if 'file' not in request.files:
        return 'No file part.', 422

    try:
        lookup = photos_uploader.save(request.files['file'], overwrite=True)
    except UploadNotAllowed as err:
        return str(err), 422

    with contextlib.suppress(IntegrityError):
        stmt = 'INSERT INTO photo (lookup) VALUES (%s)'
        db.execute(stmt, (lookup,))

    stmt = 'SELECT id, lookup, created FROM photo WHERE lookup=%s'
    photo = db.execute(stmt, (lookup,)).fetchone()
    photo['url'] = photos_uploader.get_url(lookup)

    return photo, 201


@app.delete('/<path:lookup>')
def remove(lookup):
    stmt = 'DELETE FROM photo WHERE lookup=%s'
    db.execute(stmt, (lookup,))
    photos_uploader.remove(lookup)
    return '', 204
