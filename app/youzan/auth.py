#-*- coding=utf-8 -*-
import requests
import os
import json
import time
from . import yz_config

class Auth:
    def __init__(self):
        pass

class Sign(Auth):
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def get_app_id(self):
        return self.app_id

    def get_app_secret(self):
        return self.app_secret


class Token():
    def __init__(self):
        self.server=GetToken()

    def get_token(self):
        return self.server.GetToken()

class GetToken():
    def __init__(self,client_id=yz_config.client_id,client_secret=yz_config.client_secret,shopid=yz_config.shopid):
        self.client_id=client_id
        self.client_secret=client_secret
        self.grant_type='silent'
        self.kdt_id=shopid
        self.save_path=os.path.join(os.path.abspath(__file__).replace('auth.pyc','').replace('auth.py',''),'token.json')

    def _GetToken(self):
        url='https://open.youzan.com/oauth/token'
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        data={
            'client_id':self.client_id
            ,'client_secret':self.client_secret
            ,'grant_type':self.grant_type
            ,'kdt_id':self.kdt_id
        }
        r=requests.post(url,headers=headers,data=data)
        token=json.loads(r.text)
        token['expires_in']=time.time()+24*7*3600
        with open(self.save_path,'w') as f:
            json.dump(token,f,ensure_ascii=False)
        return token.get('access_token')

    def GetToken(self):
        if not os.path.exists(self.save_path):
            return self._GetToken()
        else:
            token_file=self._ReadToken()
            if time.time()<int(token_file.get('expires_in')):
                return token_file.get('access_token')
            else:
                return self._GetToken()

    def _ReadToken(self):
        with open(self.save_path,'r') as f:
            token=json.load(f)
        return token

