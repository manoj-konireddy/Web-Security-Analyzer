import requests
from urllib.parse import urljoin


def check_securitytxt(url):

    locations = [

        "/.well-known/security.txt",

        "/security.txt"

    ]

    for location in locations:

        try:

            security_url = urljoin(url, location)

            response = requests.get(
                security_url,
                timeout=5
            )

            if response.status_code == 200:

                data = {

                    "found": True,

                    "url": security_url,

                    "status_code": 200,

                    "contact": "Not Available",

                    "expires": "Not Available",

                    "encryption": "Not Available",

                    "preferred_languages": "Not Available"

                }

                for line in response.text.splitlines():

                    line = line.strip()

                    if line.startswith("Contact:"):

                        data["contact"] = line.replace(
                            "Contact:",
                            ""
                        ).strip()

                    elif line.startswith("Expires:"):

                        data["expires"] = line.replace(
                            "Expires:",
                            ""
                        ).strip()

                    elif line.startswith("Encryption:"):

                        data["encryption"] = line.replace(
                            "Encryption:",
                            ""
                        ).strip()

                    elif line.startswith("Preferred-Languages:"):

                        data["preferred_languages"] = line.replace(
                            "Preferred-Languages:",
                            ""
                        ).strip()

                return data

        except requests.RequestException:

            continue

    return {

        "found": False,

        "url": "Not Found",

        "status_code": 404,

        "contact": "-",

        "expires": "-",

        "encryption": "-",

        "preferred_languages": "-"

    }