from urllib.parse import urlparse

class HttpClient:
    def make_http_request(self, url, method='GET', accept=None, data=None, headers=None, follow_redirects=True, max_redirects=5):

        parsed_url = self._parse_url(url)
        request_headers = self._prepare_headers(parsed_url, headers, accept)


    def _parse_url(self, url):
        """Parse url into its components."""
        parsed_url = urlparse(url)
        if not parsed_url.path:
            parsed_url = parsed_url._replace(path='/')
        return parsed_url

    def _prepare_headers(self, parsed_url, headers, accept):
        """Prepare headers for http request."""
        hostname = parsed_url.netloc
        headers['Host'] = hostname.split(':')[0]
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        headers['Connection'] = "close"
        if accept:
            headers['Accept'] = accept
        return headers

