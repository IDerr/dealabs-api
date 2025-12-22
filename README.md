# DEALABS API 

## Installation
Using pip
``` {.sourceCode .bash}
$ pip install git+https://github.com/IDerr/dealabs-api.git
```
Using source code
``` {.sourceCode .bash}
$ git clone https://github.com/IDerr/dealabs-api.git
$ cd dealabs-api
$ sudo python setup.py install
```
And voila

## CLI Commands

After installation, use the dealabs command:

### Get Hot Deals

```bash
dealabs hots [--page PAGE] [--limit LIMIT] [--days DAYS]
```

Example: `dealabs hots --limit 10 --days 7`

### Get Thread Details

```bash
dealabs get-thread THREAD_ID [--json-output]
```

Example: `dealabs get-thread 3232541 --json-output`

### Get Thread Comments

```bash
dealabs get-comments THREAD_ID [--page PAGE] [--limit LIMIT] [--sort SORT] [--json-output]
```

Example: `dealabs get-comments 3232541 --limit 20 --sort hot`

### Monitor Deals with Webhook

```bash
dealabs monitor --webhook WEBHOOK_URL [--keywords KEYWORDS...] [--categories CATEGORIES...]
```

Example:

```bash
dealabs monitor --webhook https://example.com/webhook \
  --keywords gaming \
  --categories "Video games"
```

## Use the API Programmatically

First, import the Dealabs object and models:

```python
from dealabs import Dealabs, Deal, Thread, Comment
dealabs = Dealabs()
```

### Get hot deals

```python
params = {
    "days": 1,      # 1, 7, or 30 days
    "page": 0,      # page number
    "limit": 25     # deals per page
}
response = dealabs.get_hot_deals(params=params)
deals = [Deal(deal_data) for deal_data in response.get('data', [])]

for deal in deals:
    print(f"{deal.title} - {deal.price}")
```

### Get thread details

```python
thread = dealabs.get_thread(3232541)
print(f"Title: {thread.title}")
print(f"Merchant: {thread.merchant_name}")
print(f"Temperature: {thread.temperature_rating}")
print(f"Comments: {thread.comment_count}")
```

### Get thread comments

```python
params = {"page": 0, "limit": 50, "order": "new"}
comments = dealabs.get_thread_comments(3232541, params)

for comment in comments:
    print(f"{comment.poster_username}: {comment.content_unformatted[:100]}")
```
