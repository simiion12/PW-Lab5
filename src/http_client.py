from urllib.parse import urlparse
import socket
import ssl
import gzip
import zlib


class HttpClient:
    def make_http_request(self, url, method='GET', accept=None, data=None, headers=None, follow_redirects=True, max_redirects=5):

        parsed_url = self._parse_url(url)
        request_headers = self._prepare_headers(parsed_url, headers, accept)
        request_data = self._build_request(method, parsed_url, request_headers, data)

        try:
            response, response_headers, status_code = self._send_request(parsed_url, request_data)

            if self._should_redirect(follow_redirects, status_code, response_headers, max_redirects):
                return self._handle_redirect(
                    parsed_url, response_headers, method, headers, data,
                    follow_redirects, accept, max_redirects
                )

            decoded_body = self._process_response(response, response_headers)

            return decoded_body, response_headers


        except Exception as e:
            return f"Error occurred: {str(e)}", {}


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


    def _build_request(self, method, parsed_url, request_headers, data=None):
        """Build http request."""
        path = parsed_url.path
        if parsed_url.query:
            path = path + '?' + parsed_url.query

        request = f"{method} {path} HTTP/1.1\r\n"

        for key, value in request_headers.items():
            request += key + f"\r\n{value}\r\n"

        if data:
            request += f"Content-Length: {len(data)}\r\n"

        request += f"\r\n"

        if data:
            request += data

        return request


    def _create_socket(self, parsed_url):
        """Create a socket connection."""
        hostname = parsed_url.netloc.split(':')[0]
        port = parsed_url.port if parsed_url.port else 80 if parsed_url.scheme == 'http' else 443

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if parsed_url.scheme == 'https':
            context  = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=hostname)

        sock.connect((hostname, port))
        return sock


    def _send_request(self, parsed_url, request_data):
        """Send http request."""
        s = self._create_socket(parsed_url)
        s.sendall(request_data.encode())

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

        s.close()

        # Parse response into headers and body
        headers_end = response.find(b'\r\n\r\n')
        headers_raw = response[:headers_end].encode("utf-8", errors="ignore")
        body = response[headers_end+4:]

        # Extract status code and headers
        status_line = headers_raw.split("\r\n")[0]
        status_code = int(status_line.split(" ")[1])
        response_headers = {}

        for header_line in headers_raw.split("\r\n")[1:]:
            if ":" in header_line:
                key, value = header_line.split(":", 1)
                response_headers[key.strip()] = value.strip()

        return body, response_headers, status_code


    def _should_redirect(self, follow_redirects, status_code, response_headers, max_redirects):
        """Check if we should redirect."""
        return (follow_redirects and
                status_code in (301, 302, 303, 307, 308) and
                "Location" in response_headers and
                max_redirects > 0)


    def _handle_redirect(self, parsed_url, headers, method, original_headers, data, follow_redirects, accept,
                         max_redirects):
        """Handle redirect."""
        redirect_url = headers["Location"]
        hostname = parsed_url.netloc

        # Handle relative URLs
        if not redirect_url.startswith(("http://", "https://")):
            if redirect_url.startswith("/"):
                redirect_url = f"{parsed_url.scheme}://{hostname}{redirect_url}"
            else:
                redirect_url = f"{parsed_url.scheme}://{hostname}/{redirect_url}"

        print(f"Redirecting to: {redirect_url}")
        return self.make_http_request(
            redirect_url, method, original_headers, data,
            follow_redirects, accept, max_redirects - 1
        )


    def _process_response(self, body, headers):
        """Process and decode the response body"""

        # Determine charset from Content-Type
        content_type = headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[1].split(";")[0].strip()
        if "Content-Encoding" in headers:
            body = self._decompress_body(body, headers["Content-Encoding"].lower())

        try:
            decoded_body = body.decode(charset, errors="replace")
        except (UnicodeDecodeError, LookupError):
            decoded_body = body.decode("utf-8", errors="replace")

        return decoded_body


    def _decompress_body(self, body, encoding):
        """Decompress the response body if it's compressed"""
        if encoding == "gzip":
            try:
                return gzip.decompress(body)
            except OSError:
                print("Error: Not a gzipped file")
                return body
        elif encoding == "deflate":
            try:
                return zlib.decompress(body)
            except zlib.error:
                print("Error: Not a deflated file")
                return body

        return body