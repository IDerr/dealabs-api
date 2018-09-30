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

## Use the API

Examples are available [here](https://github.com/IDerr/dealabs-api/tree/master/example)

First, import the Dealabs object 

```python
from dealabs import Dealabs
dealabs = Dealabs()
```
### Get hot deals

```python
#?days=1&page=0&limit=25
params = {
    "days": "1", # can be 1, 7 or 30 days
    "page": "1", # page number
    "limit":"25" # article per page
}
dealabs.get_deals_hot(params=params)
```
