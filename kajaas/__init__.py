# from flask import Flask
# from .index.indexkaja import index
# from ukaja.userkaja import ukaja
#
# def kaja():
#     app = Flask(__name__)
#     app.register_blueprint(index)
#     app.register_blueprint(ukaja)
#     return app
import os
from flask import Flask
from celery import Celery
from celery.task.control import revoke
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOADED_AUDIO_DEST'] = 'kajaas/static'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
basedir = os.path.abspath(os.path.dirname(__file__))

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


from kajaas.index.views import index_blueprints
from kajaas.users.views import users_blueprints
# from kaja.sponges.views import sponges_blueprints
# from kaja.errorpages.handlers import error_blueprints

app.register_blueprint(index_blueprints,url_prefix='/index')
app.register_blueprint(users_blueprints,url_prefix='/users')
# app.register_blueprint(sponges_blueprints,url_prefix='/sponges')
# app.register_blueprint(error_blueprints,url_prefix='/errorpages')

# import kaja.pindex
# import kaja.puser
# import kaja.reference.class_signup
# import kaja.reference.mongo_conn
