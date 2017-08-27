from .constants import constants as CONSTANTS



def concatenate_url_type_categories(url, typ, categories):
    if typ is not None:
        typ = CONSTANTS.API_DEAL_TYPE.format(str(typ))
        url = '{0}{1}'.format(url, type)
    if categories is not None:
        categories = CONSTANTS.API_DEAL_CATEGORIES.format(str(categories))
        url = '{0}{1}'.format(url, categories)
    return url
