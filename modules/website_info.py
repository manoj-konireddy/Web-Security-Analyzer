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

            "server": response.headers.get(
                "Server",
                "Not Available"
            ),

            "content_type": response.headers.get(
                "Content-Type",
                "Unknown"
            ),

            "powered_by": response.headers.get(
                "X-Powered-By",
                "Not Disclosed"
            ),

            "redirected": len(response.history) > 0,

            "headers": response.headers,

            "cookies": response.cookies

        }

    except requests.exceptions.MissingSchema:

        return {
            "reachable": False,
            "error": "Please enter a valid website URL."
        }

    except requests.exceptions.InvalidURL:

        return {
            "reachable": False,
            "error": "Invalid website URL."
        }

    except requests.exceptions.ConnectionError:

        return {
            "reachable": False,
            "error": "Unable to connect to the website."
        }

    except requests.exceptions.Timeout:

        return {
            "reachable": False,
            "error": "The website took too long to respond."
        }

    except requests.exceptions.TooManyRedirects:

        return {
            "reachable": False,
            "error": "The website redirected too many times."
        }

    except requests.exceptions.SSLError:

        return {
            "reachable": False,
            "error": "SSL Certificate verification failed."
        }

    except requests.exceptions.RequestException:

        return {
            "reachable": False,
            "error": "Unexpected error occurred while scanning."
        }