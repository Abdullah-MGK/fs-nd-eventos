'''
import os
import sys
import json
from flask import Flask, request, jsonify, abort
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import exc
from flask_cors import CORS

#from database.models import db_drop_and_create_all, setup_db, Event, Manager, Admin
from auth.auth import AuthError, requires_auth

from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#setup_db(app)
#CORS(app)
#CORS(app, resources={'/*': {'origins': '*'}})

# uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN

#db_drop_and_create_all()

if __name__ == '__main__':
    app.run(debug = True)
'''
