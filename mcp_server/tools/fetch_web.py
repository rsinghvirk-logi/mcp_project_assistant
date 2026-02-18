import httpx

def fetch_web(url:str) -> str:
    """
    This function allows to fetch content from a web page.
    """
    response = httpx.get(url, timetout=10) # raise a TimeoutException after 5 seconds of network inactivity
    response.raise_for_status()
    return response.text