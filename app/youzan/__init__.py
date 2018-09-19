#-*- coding=utf-8 -*-
from . import auth,yzclient,yz_config
import json


def getqr(money, tradeid, info='yaofan'):
    token = auth.Token()
    yz = yzclient.YZClient(token)
    params={}
    params['qr_name']='_'.join([info,str(tradeid)])
    params['qr_price']=money
    params['qr_type']="QR_TYPE_DYNAMIC"
    files=[]
    r=json.loads(yz.invoke('youzan.pay.qrcode.create', '3.0.0', 'GET', params=params, files=files))
    return r.get('response')

def query_trade(qr_id):
    token = auth.Token()
    yz = yzclient.YZClient(token)
    params={}
    params['qr_id']=qr_id
    files=[]
    r=json.loads(yz.invoke('youzan.trades.qr.get', '3.0.0', 'GET', params=params, files=files))
    trades=r.get('response').get('qr_trades')
    if len(trades)==0:
        return False
    else:
        trade=trades[0]
        if trade.get('status')=='TRADE_RECEIVED':
            return True
        else:
            return False

