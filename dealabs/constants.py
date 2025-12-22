from urllib.parse import urljoin

API_BASE_URL = 'https://www.dealabs.com/rest_api/v2/'
API_DEAL_SEARCH = urljoin(API_BASE_URL, 'thread/search')
API_DEAL_THREAD = urljoin(API_BASE_URL, 'thread')
API_THREAD_DETAIL = urljoin(API_BASE_URL, 'thread/{thread_id}')
API_THREAD_COMMENTS = urljoin(API_BASE_URL, 'thread/{thread_id}/comments')
