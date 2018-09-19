#-*- coding=utf-8 -*-
import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))
import pymysql


SECRET_KEY = 'sssssssssss'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')  # sqlite3
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/db' # user,password,db换成你的
SQLALCHEMY_TRACK_MODIFICATIONS = True
