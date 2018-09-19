#-*- coding=utf-8 -*-
from . import auth
import time
import requests
import hashlib

####################################
#
#   有赞开放平台SDK - Python 2.0.0
#
#      三方库依赖: requests
#
####################################

class YZClient:
    def __init__(self, authorize):
        self.auth = authorize

    def invoke(self, apiName, version, method, params={}, files={}):
        http_url = 'https://open.youzan.com/api'
        service = apiName[0: apiName.rindex('.')]
        action = apiName[apiName.rindex('.') + 1: len(apiName)]

        param_map = {}
        if isinstance(self.auth, auth.Sign):
            http_url += '/entry'
            param_map = self.get_sign(self.auth, params)
        else:
            http_url += '/oauthentry'
            param_map['access_token'] = self.auth.get_token()
            param_map = dict(list(param_map.items()) + list(params.items()))

        http_url = http_url + '/' + service + '/' + version + '/' + action

        resp = self.send_request(http_url, method, param_map, files)
        if resp.status_code != 200:
            print(resp.status_code)
            raise Exception('Invoke failed')
        return resp.content

    def send_request(self, url, method, param_map, files):
        headers_map = {
            'User-Agent': 'X-YZ-Client 2.0.0 - Python'
        }
        if method.upper() == 'GET':
            return requests.get(url=url, params=param_map, headers=headers_map)
        elif method.upper() == 'POST':
            return requests.post(url=url, data=param_map, files=files, headers=headers_map)

    def get_sign(self, sign, params):
        if not isinstance(sign, auth.Sign):
            raise Exception('Sign mode must specify typeof auth.Sign')
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        format = 'json'
        app_id = sign.get_app_id()
        app_secret = sign.get_app_secret()
        v = '1.0'
        sign_method = 'md5'

        param_map = {
            'timestamp': timestamp,
            'format': format,
            'app_id': app_id,
            'app_secret': app_secret,
            'v': v,
            'sign_method': sign_method
        }

        param_map=dict(param_map.items() + params.items())
        sorted_param_map = sorted(param_map.items(), key = lambda d : d[0])
        plain_text = app_secret
        for item in sorted_param_map:
            plain_text += (item[0] + item[1])
        plain_text += app_secret
        md5 = hashlib.md5(plain_text).hexdigest()
        param_map['sign'] = md5

        return param_map
