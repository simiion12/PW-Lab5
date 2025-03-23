from urllib.parse import urlparse

class HttpClient:
    def make_http_request(self, url, method='GET', accept=None, data=None, headers=None, follow_redirects=True, max_redirects=5):

        parsed_url = self._parse_url(url)


    def _parse_url(self, url):
        """Parse url into its components."""
        parsed_url = urlparse(url)
        if not parsed_url.path:
            parsed_url = parsed_url._replace(path='/')
        return parsed_url

