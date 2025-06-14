import requests
from requests_oauthlib import OAuth1
from .constants import *
from .models import Deal


class Dealabs:

    def __init__(self):
        self.client_key = "539f008401dbb"
        self.client_secret = "539f008401e9c"
        self.headers = {
            'User-Agent': 'com.dealabs.apps.android ANDROID [v7.19.00] [22 | SM-G930K] [@2.0x]',
            'Pepper-Include-Counters': 'unread_alerts',
            'Pepper-Include-Prev-And-Next-Ids': 'true',
            'Pepper-JSON-Format': 'thread=list,group=ids,type=light,event=light,user=full,badge=user,formatted_text=html,message=with_code',
            'Pepper-Hardware-Id': '5bce296a65215d0bb3b9751bb77b0a1d',
            'Host': 'www.dealabs.com',
        }
        self.oauth = OAuth1(self.client_key, client_secret=self.client_secret)

    def request(self, url, method='GET', params={}):
        r = requests.request(method=method, url=url, params=params, headers=self.headers, auth=self.oauth).json()
        return r

    def get_hot_deals(self, params={}):
        # TODO: check params
        # ex: ?days=1&page=0&limit=25
        new_options = {
            'order_by' : 'hot',
            'limit':'50'
        }
        params = {**new_options, **params}
        return self.request(url=API_DEAL_THREAD, params=params)

    def search_deals(self, params):
        # TODO: check params
        # ex: ?order_by=new&type_id=&query=&page=&group_id=&merchant_id=&limit=25&expired=&local=&clearance=
        # order_by = "new", "hot", "discussed", "featured", "new"
        new_options = {
            'order_by' : 'hot',
            'limit':'50'
        }
        return self.request(url=API_DEAL_SEARCH, params=params)
      
    def get_new_deals(self, params={}):
        new_options = {
            'order_by' : 'new',
            'limit':'50'
        }
        params = {**new_options, **params}
        req = self.request(url=API_DEAL_THREAD, params=params)
        deals_data = req.get('data', [])
        return [Deal(deal_data) for deal_data in deals_data]
