import requests
from requests_oauthlib import OAuth1
from .constants import *
from .models import Deal, Thread, Comment


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

    def get_thread(self, thread_id, params={}):
        """
        Fetch detailed information about a specific thread.

        Args:
            thread_id: The ID of the thread to fetch
            params: Optional query parameters

        Returns:
            Thread object with detailed information
        """
        url = API_THREAD_DETAIL.format(thread_id=thread_id)
        response = self.request(url=url, params=params)
        thread_data = response.get('data', {})
        return Thread(thread_data)

    def get_thread_comments(self, thread_id, params={}):
        """
        Fetch comments for a specific thread.

        Args:
            thread_id: The ID of the thread to fetch comments for
            params: Optional query parameters (e.g., page, limit, order)

        Returns:
            List of Comment objects
        """
        url = API_THREAD_COMMENTS.format(thread_id=thread_id)
        response = self.request(url=url, params=params)
        comments_data = response.get('data', [])
        return [Comment(comment_data) for comment_data in comments_data]
