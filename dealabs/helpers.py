from .constants import API_DEAL_TYPE, API_DEAL_CATEGORIES



def concatenate_url_type_categories(url, typ, categories):
    if typ is not None:
        typ = API_DEAL_TYPE.format(str(typ))
        url = '{0}{1}'.format(url, type)
    if categories is not None:
        categories = API_DEAL_CATEGORIES.format(str(categories))
        url = '{0}{1}'.format(url, categories)
    return url
