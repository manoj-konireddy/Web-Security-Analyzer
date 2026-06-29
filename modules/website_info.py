import requests
import time


def get_website_info(url):

    try:

        start_time = time.time()

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        response_time = round(
            (time.time() - start_time) * 1000,
            2
        )

        return {
            "reachable": True,
            "url": response.url,
            "status_code": response.status_code,
            "response_time": response_time,
            "server": response.headers.get("Server", "Not Available"),
            "content_type": response.headers.get("Content-Type", "Unknown"),
            "powered_by": response.headers.get("X-Powered-By", "Not Disclosed"),
            "redirected": len(response.history) > 0,
            "headers": response.headers
        }

    except requests.exceptions.RequestException as error:

        return {
            "reachable": False,
            "error": str(error)
        }