import requests
import time


def get_website_info(url):
    """
    Fetch basic information about the target website.
    """

    try:
        start = time.time()

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        end = time.time()

        return {
            "url": response.url,
            "status_code": response.status_code,
            "response_time_ms": round((end - start) * 1000, 2),
            "server": response.headers.get("Server", "Unknown"),
            "content_type": response.headers.get("Content-Type", "Unknown"),
            "powered_by": response.headers.get("X-Powered-By", "Not Disclosed"),
            "redirected": response.history != [],
            "reachable": True,
            "headers": dict(response.headers)
        }

    except Exception as e:

        return {
            "reachable": False,
            "error": str(e)
        }