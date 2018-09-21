#-*- coding=utf-8 -*-
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.sql import func
from app import *
from app.models import *
from sqlalchemy import func as SQLfunc
import logging
import re
import hashlib
import datetime

def today():
    now=datetime.datetime.now().strftime('%Y%m%d')
    now_f=datetime.datetime.strptime(now,'%Y%m%d')
    return now_f

def yesterday():
    now=(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y%m%d')
    now_f=datetime.datetime.strptime(now,'%Y%m%d')
    return now_f


def YaoFanJiLu(num=10):
    orders=Order.query.order_by(Order.starttime.desc()).limit(num)
    return orders


def YaoFan_total():
    num_today=Order.query.filter(Order.trade_status==True,Order.starttime>=today()).count()
    money_today=db.session.query(func.sum(Order.money).label('money_today')).filter(Order.trade_status==True,Order.starttime>=today()).first().money_today
    num_yesterday=Order.query.filter(Order.trade_status==True,Order.starttime>=yesterday(),Order.starttime<today()).count()
    money_yesterday=db.session.query(func.sum(Order.money).label('money_yesterday')).filter(Order.trade_status==True,Order.starttime>=yesterday(),Order.starttime<today()).first().money_yesterday
    num_total=Order.query.filter(Order.trade_status==True).count()
    money_total=db.session.query(func.sum(Order.money).label('money_total')).filter(Order.trade_status==True).first().money_total
    if money_today is None:
        money_today=0
    else:
        money_today=round(money_today,2)
    if money_yesterday is None:
        money_yesterday=0
    else:
        money_yesterday=round(money_yesterday,2)
    if money_total is None:
        money_total=0
    else:
        money_total=round(money_total,2)
    return num_today,money_today,num_yesterday,money_yesterday,num_total,money_total


manager = Manager(app)
migrate = Migrate(app, db)
app.jinja_env.globals['qq'] = '228812493'
app.jinja_env.globals['domain'] = 'https://iofaka.com'
app.jinja_env.globals['YaoFanJiLu'] = YaoFanJiLu
app.jinja_env.globals['YaoFan_total'] = YaoFan_total



def make_shell_context():
    return dict(app=app, db=db, IP=IP, ID=ID, Context=Context, Post=Post, clPost=clPost, Role=Role, User=User, FriendUrl=FriendUrl)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    print('init success!')


manager.add_command('Shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
