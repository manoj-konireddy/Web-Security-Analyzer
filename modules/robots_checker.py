import requests
from urllib.parse import urljoin


def check_robots(url):

    try:

        robots_url = urljoin(url, "/robots.txt")

        response = requests.get(
            robots_url,
            timeout=5
        )

        if response.status_code == 200:

            lines = response.text.strip().splitlines()

            return {

                "found": True,

                "url": robots_url,

                "status_code": response.status_code,

                "rules": len(lines)

            }

        return {

            "found": False,

            "url": robots_url,

            "status_code": response.status_code,

            "rules": 0

        }

    except Exception as error:

        return {

            "found": False,

            "url": "",

            "status_code": "Error",

            "rules": 0,

            "error": str(error)

        }