from models.scan_result import ScanResult

from modules.website_info import get_website_info
from modules.security_headers import analyze_security_headers

def start_scan(url):

    scan = ScanResult()

    scan.website = get_website_info(url)

    if not scan.website["reachable"]:

        print("Unable to connect.")

        return

    scan.headers = analyze_security_headers(
        scan.website["headers"]
    )

    return scan