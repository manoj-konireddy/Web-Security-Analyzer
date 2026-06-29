from utils.banner import print_banner

from scanner import start_scan


def main():

    print_banner()

    url = input("\nEnter Website URL: ").strip()

    if not url.startswith(("http://", "https://")):

        print("Invalid URL")

        return

    scan = start_scan(url)

    print("\nScan Completed Successfully\n")

    print(scan.website)

    print()

    print(scan.headers)


if __name__ == "__main__":

    main()