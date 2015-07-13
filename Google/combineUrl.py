def combineUrl(api, params):
    """
    Create a request url by concatenating API url and parameters.
    
    Args:
      (String) api: the url for API
      (dict) params: the parameters for the request
    Return:
      a string of combined url
    """
    url = api 
    length = len(params)
    for i, param in enumerate(params):
        url += param + "=" + params[param]
        if i < length-1:
            url += "&"
    return url