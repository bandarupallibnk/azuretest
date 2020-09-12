from flask import Flask,jsonify,request,session,render_template
import jwt,datetime
from functools import wraps
from kajaas import app

class clsjwtprocess():

    def checkfortoken(func):
        @wraps(func)
        def wrapped(*args,**kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'message':'missing token'}),403
            try:
                data = jwt.decode(token,app.config['SECRET_KEY'])
            except:
                return jsonify({'message':'Invalid Token'}),403
            # data = jwt.decode(token,app.config['SECRET_KEY'])
            return func(*args,**kwargs)
        return wrapped
