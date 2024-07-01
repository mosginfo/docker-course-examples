from flask import abort, current_app, g, Flask
import pymysql


class PyMySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def get_app(self):
        if self.app is not None:
            return self.app
        return current_app

    def init_app(self, app: Flask):
        app.config.setdefault('MYSQL_HOST', 'localhost')
        app.config.setdefault('MYSQL_USER', None)
        app.config.setdefault('MYSQL_PASSWORD', None)
        app.config.setdefault('MYSQL_DATABASE', None)
        app.config.setdefault('MYSQL_CURSOR_CLASS', 'DictCursor')
        app.teardown_appcontext(self.close_connection)

    def close_connection(self, exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    @property
    def connection(self):
        if 'db' not in g:
            app = self.get_app()
            g.db = pymysql.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DATABASE'],
                cursorclass=getattr(pymysql.cursors, app.config['MYSQL_CURSOR_CLASS'])
            )
        return g.db

    def execute(self, stmt, args=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(stmt, args)
                return cursor
            except pymysql.MySQLError as err:
                self.connection.rollback()
                abort(500, str(err))
            finally:
                self.connection.commit()
