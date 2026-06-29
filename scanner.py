from modules.website_info import get_website_info
from modules.security_headers import check_security_headers
from modules.ssl_checker import check_ssl
from modules.cookie_analyzer import analyze_cookies
from modules.http_methods import check_http_methods
from modules.robots_checker import check_robots
from modules.securitytxt_checker import check_securitytxt


def start_scan(url):

    result = {}

    website = get_website_info(url)

    result["website"] = website

    if website["reachable"]:

        result["security_headers"] = check_security_headers(
            website["headers"]
        )

        result["ssl"] = check_ssl(url)
        result["cookies"] = analyze_cookies(
            website["cookies"]
        )
        result["http_methods"] = check_http_methods(url)
        result["robots"] = check_robots(url)
        result["securitytxt"] = check_securitytxt(url)

    return result