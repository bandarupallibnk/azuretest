from flask import Flask,render_template,redirect,url_for,request,session,Blueprint
from flask_wtf import FlaskForm
from wtforms import SubmitField
from kajaas.index.forms import clsignup,clslogin,clsspongesignup,clsspongelogin
from kajaas.mongo_conn import clsmongo
from kajaas.clsjwt import clsjwtprocess
import psycopg2
import ast, re
from kajaas.edate import cl_date
import hashlib
from kajaas import app
import os,jwt
import jwt,datetime


index_blueprints = Blueprint('index',__name__,template_folder='templates')
#app = Flask(__name__)
#index = Blueprint('indexkaja',__name__)
#app.config['SECRET_KEY'] = 'mysecretkey'

class clindex(FlaskForm):
    signup = SubmitField("Sign Up")
    login = SubmitField("Log In")

class clspongindex(FlaskForm):
    ssignup = SubmitField("Sign Up")
    slogin = SubmitField("Log In")

def verifynotempty(entry):
    if entry :
        return False
    else:
        return True

def verifydateformat(value):
    date_format = '%d-%m-%Y'
    try:
      date_obj = datetime.datetime.strptime(value, date_format)
      return False
    except ValueError:
      return True

def calculateage(value):
    date_format = '%d-%m-%Y'
    date_obj = datetime.datetime.strptime(value, date_format)
    val = str(datetime.datetime.now()-date_obj)
    return int(int(val.split(' ')[0])/365)

# Encrypting password
def hashing(password):
    bpwd = str.encode(password)
    vhashed = hashlib.sha512(bpwd)
    return vhashed.hexdigest()

#db connection
def pgconn():
    fopen = open('/Users/nandabandarupalli/Documents/kaja/kaja/static/pgcreds','r')
    creds = fopen.read()
    dictionary = ast.literal_eval(creds)
    conn = psycopg2.connect(host=dictionary.get('v_host'),database=dictionary.get('v_database'),user=dictionary.get('v_user'),password=dictionary.get('v_password'))
    return conn

#insert into database
def inssignup(firstname,email,username,password,ageo18):
    try:
        dt = cl_date()
        regtime = dt.futcdatetime()
        newpass = password + regtime
        conn = pgconn()
        cur = conn.cursor()
        hashedpwd = hashing(newpass)
        insertsql = "insert into dbkaja.{} (firstname,email,username,userpassword,agebool,regtime) values ('{}','{}','{}','{}',{},'{}') ".format('tblkaja',firstname,email,username,hashedpwd,ageo18,regtime)
        cur.execute(insertsql)
        conn.commit()
        cur.close()
        conn.close()
        return 'good'
    except psycopg2.errors.UniqueViolation as e:
        mess = str(e)
        print(mess)
        if re.match(".*email.*", mess):
            return 'email'
        elif re.match(".*username.*", mess):
            return 'username'

def inssponge(firstname,middlename,lastname,dob,gender,email,username,userpassword):
    try:
        dt = cl_date()
        regtime = dt.futcdatetime()
        newpass = userpassword + regtime
        conn = pgconn()
        cur = conn.cursor()
        hashedpwd = hashing(newpass)
        insertsql = "insert into dbkaja.{} (firstname,middlename,lastname,dob,gender,email,username,userpassword,regtime) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}') ".format('tblsponges',firstname,middlename,lastname,dob,gender,email,username,hashedpwd,regtime)
        cur.execute(insertsql)
        conn.commit()
        cur.close()
        conn.close()
        return 'good'
    except psycopg2.errors.UniqueViolation as e:
        mess = str(e)
        print(mess)
        if re.match(".*email.*", mess):
            return 'email'
        elif re.match(".*username.*", mess):
            return 'username'

def verifyuser(uname,upass):
    conn = pgconn()
    cur = conn.cursor()
    selectsql = "select userpassword,regtime from dbkaja.tblkaja where username='{}'".format(uname)
    cur.execute(selectsql)
    data = cur.fetchall()
    if len(data) == 1:
        if data[0][0] == hashing(upass + data[0][1]):
            return True
        else:
            return False
def verifysponge(uname,upass):
    conn = pgconn()
    cur = conn.cursor()
    selectsql = "select userpassword,regtime from dbkaja.tblsponges where username='{}'".format(uname)
    cur.execute(selectsql)
    data = cur.fetchall()
    if len(data) == 1:
        if data[0][0] == hashing(upass + data[0][1]):
            return True
        else:
            return False

def verifyusernameavailable(uname,tblname):
    try:
        conn = pgconn()
        cur = conn.cursor()
        selectsql = "select userpassword,regtime from dbkaja.{} where username='{}'".format(tblname,uname)
        cur.execute(selectsql)
        data = cur.fetchall()
        if len(data) > 0:
            return False
        else:
            return True
    except:
        return False

def verifyemailavailable(email,tblname):
    try:
        conn = pgconn()
        cur = conn.cursor()
        selectsql = "select userpassword,regtime from dbkaja.{} where email='{}'".format(tblname,email)
        cur.execute(selectsql)
        data = cur.fetchall()
        if len(data) > 0:
            return False
        else:
            return True
    except:
        return False


def insmongo(username):
    mobj = clsmongo()
    dt = cl_date()
    lgtime = dt.futcdatetime()
    mtoken = hashing(username+lgtime)
    mobj.activateuser(username,mtoken)

def encode_auth_token(self, username):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

@index_blueprints.route('/index',methods=['GET','POST'])
# @app.route('/',methods=['GET','POST'])
def index():
    index = clindex()
    if index.validate_on_submit():
        if index.signup.data:
            return redirect('index/signup')
        elif index.login.data:
            return redirect('index/login')
    return render_template('index.html',form=index)

@index_blueprints.route('/signup',methods=['GET','POST'])
# @app.route('/signup',methods=['GET','POST'])
def signup():
    objsignup = clsignup()
    lcheck = []
    if objsignup.validate_on_submit():
        session['username'] = objsignup.username.data
        session['password'] = objsignup.password.data
        session['firstname'] = objsignup.firstname.data
        session['lastname'] = objsignup.lastname.data
        session['email'] = objsignup.email.data
        session['ageo18'] = objsignup.ageo18.data

        if verifynotempty(session['username']):
            lcheck.append('username not valid')
        if verifynotempty(session['password']):
            lcheck.append('password not valid')
        if verifynotempty(session['firstname']):
            lcheck.append('firstname not valid')
        if verifynotempty(session['ageo18']):
            lcheck.append('Please confirm your age')
        if not(verifyusernameavailable(session['username'],'tblkaja')):
            lcheck.append("User Id already taken")
            # return render_template('signup.html',form=objsignup,lcheck = lcheck)
        if not(verifyemailavailable(session['email'],'tblkaja')):
            lcheck.append("Email already taken")
            # return render_template('signup.html',form=objsignup,lcheck = lcheck)
        if len(lcheck) > 0:
            return render_template('signup.html',form=objsignup,lcheck = lcheck)
        result = inssignup(session['firstname'],session['email'],session['username'],session['password'],session['ageo18'])
        return redirect(url_for('index.login'))
    return render_template('signup.html',form=objsignup,lcheck = lcheck)

@index_blueprints.route('/login',methods=['GET','POST'])
# @app.route('/login',methods=['GET','POST'])
def login():
    objlogin = clslogin()
    mobj = clsmongo()
    lcheck = []
    if objlogin.validate_on_submit():
        session['username'] = objlogin.username.data
        session['password'] = objlogin.password.data
        if not(session['username']):
            lcheck.append('Enter Username')
        if not(session['password']):
            lcheck.append('Enter password')
        if len(lcheck) == 0:
            if verifyuser(session['username'],session['password']):
                session['logged_in'] = True
                token = jwt.encode({
                    'user':session['username'],
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=6000)
                },
                app.config['SECRET_KEY'])
                session['token'] = token.decode('utf-8')
                session['is_active'] = True
                return redirect(url_for('users.uhome',token = session['token']))
            else:
                lcheck.append('Invalid Username or password')
                return render_template('login.html',form=objlogin,lcheck = lcheck)
    return render_template('login.html',form=objlogin,lcheck = lcheck,curdir=os.curdir)
