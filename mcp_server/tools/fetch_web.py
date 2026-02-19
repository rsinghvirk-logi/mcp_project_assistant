import httpx
import truststore
truststore.inject_into_ssl()

def fetch_web(url:str) -> str:
    """
    This function allows to fetch content from a web page.
    """
    response = httpx.get(url, timetout=10) # raise a TimeoutException after 10 seconds of network inactivity
    response.raise_for_status()
    return response.text # will be the HTML (same as view page source)