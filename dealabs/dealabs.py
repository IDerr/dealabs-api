import requests
from requests_oauthlib import OAuth1
from .constants import *


class Dealabs:

    def __init__(self):
        self.client_key = "539f008401dbb"
        self.client_secret = "539f008401e9c"
        self.headers = {"Dealabs-App-Version": "com.dealabs.apps.android:82"}
        self.oauth = OAuth1(self.client_key, client_secret=self.client_secret)

    def request(self, url, method='GET', params={}):
        r = requests.request(method=method, url=url, params=params, headers=self.headers, auth=self.oauth).json()
        return r

    def get_deals_hot(self, params={}):
        # TODO: check params
        # ex: ?days=1&page=0&limit=25
        return self.request(url=API_DEAL_HOTTEST, params=params)

    def search_deals(self, params):
        # TODO: check params
        # ex: ?order_by=new&type_id=&query=&page=&group_id=&merchant_id=&limit=25&expired=&local=&clearance=
        # order_by = "new", "hot", "discussed", "featured", "new"
        return self.request(url=API_DEAL_SEARCH, params=params)
    
    def search_merchant(self, params):
        # TODO: check params
        # ex: query=urlencoded(search)&page=int>1&limit=25
        return self.request(url=API_MERCHANT_SEARCH, params=params)