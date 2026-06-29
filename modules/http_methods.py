import requests


HTTP_METHODS = [
    "GET",
    "POST",
    "HEAD",
    "OPTIONS",
    "PUT",
    "DELETE"
]


def check_http_methods(url):

    supported_methods = []

    for method in HTTP_METHODS:

        try:

            response = requests.request(
                method=method,
                url=url,
                timeout=5
            )

            if response.status_code != 405:

                supported_methods.append({

                    "method": method,

                    "supported": True,

                    "status": response.status_code

                })

            else:

                supported_methods.append({

                    "method": method,

                    "supported": False,

                    "status": response.status_code

                })

        except requests.exceptions.RequestException:

            supported_methods.append({

                "method": method,

                "supported": False,

                "status": "Error"

            })

    return supported_methods