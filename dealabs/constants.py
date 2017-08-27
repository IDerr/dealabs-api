from urllib.parse import urljoin


RESULTS = 50
API_BASE_URL = 'http://api.dealabs.com/api/v1/'
API_DEAL_HOT = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=hot')
API_DEAL_NEW = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=new')
API_DEAL_DISCUSSED = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=discussed')
API_DEAL_COMMENT_NOTIFICATIONS = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=comment_notifications')
API_DEAL_ALERT_NOTIFICATIONS = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=alert_notifications')
API_DEAL_ALERTS = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=alerts')
API_DEAL_SEARCH = urljoin(API_BASE_URL, 'deal?per_page={0}&tab=new&search={1}')
API_DEAL_COMMENTS = urljoin(API_BASE_URL, 'deal/{0}/comments?per_page={1}')
API_DEAL_TYPE = '&type={0}'
API_DEAL_CATEGORIES = '&categories={0}'
API_CATEGORY = urljoin(API_BASE_URL, 'category')
API_REGION = urljoin(API_BASE_URL, 'deal/regions')
API_MEMBER_DEALS = urljoin(API_BASE_URL, 'member/{0}/deals?per_page={1}')
API_MEMBER_COMMENTS = urljoin(API_BASE_URL, 'member/{0}/comments?per_page={1}')
