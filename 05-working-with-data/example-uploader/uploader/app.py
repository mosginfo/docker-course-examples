from flask import (
    Flask,
    flash,
    redirect,
    request,
    render_template,
    url_for,
)
from flask_uploader import init_uploader
from flask_uploader import Uploader
from flask_uploader.exceptions import UploadNotAllowed
from flask_uploader.storages import FileSystemStorage, iter_files
from flask_uploader.validators import (
    Extension,
    FileRequired,
    FileSize,
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Very secret string'
app.config['UPLOADER_ROOT_DIR'] = '/upload'
app.config.from_prefixed_env()
init_uploader(app)

photos_storage = FileSystemStorage(dest='.')
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
    return render_template('index.html', files=iter_files(photos_storage))


@app.post('/remove/<path:lookup>')
def remove(lookup):
    photos_uploader.remove(lookup)
    return redirect(url_for('index'))


@app.post('/')
def upload():
    if 'file' not in request.files:
        flash('No file part.')
        return redirect(request.url)

    try:
        lookup = photos_uploader.save(request.files['file'], overwrite=True)
        flash(f'Photo saved successfully - {lookup}.')
    except UploadNotAllowed as err:
        flash(str(err))

    return redirect(request.url)
