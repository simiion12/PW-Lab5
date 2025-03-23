import argparse

from src.http_client import HttpClient

def main():
    parser = argparse.ArgumentParser(description='A simple web scraping tool')
    parser.add_argument('-u', '--url', help='Fetch the given URL')
    parser.add_argument('-s', '--search', help='Search term to look for')
    parser.add_argument('-link', type=int, help='Link number from search result')
    parser.add_argument("--json", action="store_true", help="Request JSON content")
    parser.add_argument("--html", action="store_true", help="Request HTML content")

    args = parser.parse_args()

    client = HttpClient()

    if args.url:
        # Request format
        accept = None
        if args.json:
            accept = "application/json"
        elif args.html:
            accept = "text/html"

        response = client.make_http_request(args.url, accept=accept)

    elif args.search:
        pass
    elif args.link:
        pass
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
