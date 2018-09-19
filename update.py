#-*- coding=utf-8 -*-
from app.youzan import query_trade
from app.models import Order
import datetime

def Check():
    time=datetime.datetime.now()+datetime.timedelta(minutes=-10)
    orders=Order.query.filter(Order.starttime>=time,Order.trade_status==False).all()
    print('-----------{} orders waiting to check-----------'.format(len(orders)))
    for order in orders:
        print('----------check order {}---------'.format(order.trade_id))
        trade_status=query_trade(order.qr_id)
        if trade_status == True:
            # 订单信息更新
            order.endtime = datetime.datetime.now()
            order.trade_status = True
            db.session.add(order)
            db.session.commit()

if __name__=='__main__':
    Check()
