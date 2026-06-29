import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime


def check_ssl(url):

    try:

        hostname = urlparse(url).hostname

        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=10) as sock:

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                certificate = ssock.getpeercert()

        issuer = dict(x[0] for x in certificate["issuer"])

        issued_to = dict(x[0] for x in certificate["subject"])

        valid_from = datetime.strptime(
            certificate["notBefore"],
            "%b %d %H:%M:%S %Y %Z"
        )

        valid_until = datetime.strptime(
            certificate["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        remaining_days = (valid_until - datetime.utcnow()).days

        return {

            "enabled": True,

            "valid": remaining_days > 0,

            "issuer": issuer.get("organizationName", "Unknown"),

            "issued_to": issued_to.get("commonName", hostname),

            "valid_from": valid_from.strftime("%d-%b-%Y"),

            "valid_until": valid_until.strftime("%d-%b-%Y"),

            "days_remaining": remaining_days

        }

    except Exception as error:

        return {

            "enabled": False,

            "error": str(error)

        }