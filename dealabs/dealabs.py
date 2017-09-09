from requests_oauthlib import OAuth1
import requests

from .helpers import concatenate_url_type_categories
from .constants import *


class Dealabs:

    def __init__(self):
        self.client_key = "539f008401dbb"
        self.client_secret = "539f008401e9c"
        self.headers = {"Dealabs-App-Version": "com.dealabs.apps.android:82"}
        self.oauth = OAuth1(self.client_key, client_secret=self.client_secret)

    def request(self, url, method='GET', data=None):
        r = requests.request(method=method, url=url, data=data, headers=self.headers, auth=self.oauth).json()
        return r

    def get_categories(self):
        url = API_CATEGORY
        return self.request(url=url)

    def get_regions(self):
        url = API_REGION
        return self.request(url=url)

    def get_member_deals(self, member_id, results=RESULTS):
        url = API_MEMBER_DEALS.format(str(member_id), str(results))
        return self.request(url=url)

    def get_member_comments(self, member_id, results=RESULTS):
        url = API_MEMBER_COMMENTS.format(str(member_id), str(results))
        return self.request(url=url)

    def get_deal_comments(self, deal_id, results=RESULTS):
        url = API_DEAL_COMMENTS.format(str(deal_id), str(results))
        return self.request(url=url)

    def get_deals_hot(self, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_HOT.format(str(results))
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)

    def get_deals_new(self, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_NEW.format(str(results))
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)

    def get_deals_discussed(self, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_DISCUSSED.format(str(results))
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)

    def get_deals_comment_notifications(self, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_COMMENT_NOTIFICATIONS.format(str(results))
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)

    def get_deals_alert_notifications(self, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_ALERT_NOTIFICATIONS.format(str(results))
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)

    def get_deals_alerts(self, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_ALERTS.format(str(results))
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)

    def search_deals(self, search, typ=None, categories=None, results=RESULTS):
        url = API_DEAL_SEARCH.format(str(results), search)
        url = concatenate_url_type_categories(url, typ, categories)
        return self.request(url=url)
