# -*- coding=utf-8 -*-
from app import db
import datetime

# order
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    trade_id = db.Column(db.String(64), index=True)
    qr_id = db.Column(db.String(64), index=True)
    trade_status = db.Column(db.Boolean, default=False)
    starttime = db.Column(db.DateTime, default=datetime.datetime.now)
    endtime = db.Column(db.DateTime)
    money=db.Column(db.Float)


    def __repr__(self):
        return self.trade_id
