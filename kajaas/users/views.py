from flask import Flask,render_template,url_for,redirect,Blueprint,url_for,session,make_response,jsonify,request
from flask_wtf import FlaskForm
from kajaas import app,celery
from kajaas.users.forms import clsupload
from kajaas.mongo_conn import clsmongo
from kajaas.clsjwt import clsjwtprocess
import jwt,datetime,time
from edate import cl_date
from datetime import timedelta
from celery.task.control import revoke
from flask_uploads import configure_uploads,IMAGES,AUDIO,UploadSet

audio = UploadSet('audio',AUDIO)
configure_uploads(app,audio)

users_blueprints = Blueprint('users',__name__,template_folder='templates')
requeststatus = 'expired'

def verifynotempty(entry):
    if entry :
        return False
    else:
        return True

@users_blueprints.route('/uhome',methods=['GET','POST'])
@clsjwtprocess.checkfortoken
def uhome():
    data = jwt.decode(session['token'],app.config['SECRET_KEY'])
    session['username'] = data['user']
    dt = cl_date()
    logintime = dt.futcdatetime()
    mobj = clsmongo()
    mobj.activateuser(data['user'],logintime,session['token'])
    laudios = mobj.retrieveaudio()
    # rstatus,spongename = mobj.checkuserrequeststatus(session['username'])
    # print(session['userrequest'])
    return render_template('uhome.html',username=session['username'].capitalize(),laudios=laudios)


@users_blueprints.route('/logoff')
@clsjwtprocess.checkfortoken
def logoff():
    dt = cl_date()
    logofftime = dt.futcdatetime()
    mobj = clsmongo()
    mobj.logoffuser(session['username'],logofftime)
    session['token'] = ''
    session['is_active'] = False
    session['userrequest'] = "expired"
    return redirect(url_for('index.index'))

@users_blueprints.route('/upload',methods=['GET','POST'])
@clsjwtprocess.checkfortoken
def upload():
    objprofile = clsupload()
    data = jwt.decode(session['token'],app.config['SECRET_KEY'])
    username=data['user']
    filename = ''
    print('Hello I am outside')
    if objprofile.validate_on_submit():
        print('Hello I am inside')
        mobj = clsmongo()
        session['aboutaudio'] = objprofile.aboutaudio.data
        print('This is about audio {}'.format(session['aboutaudio']))
        filename = ''
        if objprofile.audio.data:
            filename = audio.save(objprofile.audio.data,name=username + ".")
            # return redirect(url_for('users.uhome',token = session['token']))
        if not(verifynotempty(session['aboutaudio'])) and filename != '' :
            print('Hello I am doubleinsede')
            mobj.uploadaudio(data['user'],session['aboutaudio'],filename)
            return redirect(url_for('users.uhome',token = session['token']))
    return render_template('upload.html',form=objprofile,token = session['token'],
    username=username.capitalize())

@users_blueprints.route('/uhome/playaudio',methods=['POST'])
@clsjwtprocess.checkfortoken
def fplayaudio():
    mobj = clsmongo()
    dt = cl_date()
    req = request.get_json()
    results = mobj.getspecificaudio(req["uname"],req["fname"])
    for res in results:
        fname = res["filename"]
        atitle = res["audiotitle"]
        print(res["filename"])
    return jsonify({}), 200, {'atitle':atitle,'fname':fname}
