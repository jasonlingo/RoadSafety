def combineUrl(api, params):
    """
    Create a request url by concatenating API url and parameters.
    
    Args:
      (String) api: the url for API.
      (dictionary) params: the parameters for the request.
    Return:
      (String) combined url.
    """

    url = api 

    # Get the number of parameters.
    length = len(params)
    for i, param in enumerate(params):
        # Add i-th parameter to the url.
        url += param + "=" + params[param]
        if i < length - 1:
            # Add an "&" between every two parameters. 
            # Don't add it at the end of the url.
            url += "&"
            
    return url