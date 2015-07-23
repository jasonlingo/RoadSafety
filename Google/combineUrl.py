def combineUrl(api, params):
    """
    Create a request url by concatenating API url and parameters.
    
    Args:
      (String) api: the url of a API.
      (dictionary) params: the parameters for the request.
    Return:
      (String) combined url.
    """
    # Create a parameter list.
    request = [api] 

    for param in params:
        # Add i-th parameter to the list.
        request.append(param + "=" + params[param])
    
    # Join every item in the requestUrl list to be a string
    # with a "&" word between two parameters.
    requestUrl = "&".join(request)
    
    return requestUrl