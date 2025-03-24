import argparse

from src.http_client import HttpClient
from src.formatters import Formatter

def main():
    parser = argparse.ArgumentParser(description='A simple web scraping tool')
    parser.add_argument('-u', '--url', help='Fetch the given URL')
    parser.add_argument('-s', '--search', help='Search term to look for')
    parser.add_argument('-link', type=int, help='Link number from search result')
    parser.add_argument("--json", action="store_true", help="Request JSON content")
    parser.add_argument("--html", action="store_true", help="Request HTML content")

    args = parser.parse_args()

    client = HttpClient()
    formatter = Formatter()

    if args.url:
        # Request format
        accept = None
        if args.json:
            accept = "application/json"
        elif args.html:
            accept = "text/html"

        response, headers = client.make_http_request(args.url, accept=accept)

        content_type = headers.get("Content-Type", "")
        if "application/json" in content_type:
            print(formatter.format_json_content(response))
        else:
            formatter.format_html_content(response)

    elif args.search:
        pass
    elif args.link:
        pass
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
