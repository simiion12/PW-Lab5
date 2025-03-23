import argparse


def main():
    parser = argparse.ArgumentParser(description='A simple web scraping tool')
    parser.add_argument('-u', '--url', help='Fetch the given URL')
    parser.add_argument('-s', '--search', help='Search term to look for')
    parser.add_argument('-link', type=int, help='Link number from search result')

    args = parser.parse_args()



if __name__ == '__main__':
    main()
