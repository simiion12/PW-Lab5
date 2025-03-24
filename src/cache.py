import os
import json
import datetime


class Cache:
    def __init__(self, cache_dir=".go2web_cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def get_cache_path(self, url, content_type=None):
        # Create a filename based on the URL
        filename = url.replace("://", "_").replace("/", "_").replace("?", "_").replace("&", "_")
        if content_type:
            filename += f"_{content_type}"
        return os.path.join(self.cache_dir, filename)

    def get(self, url, content_type=None, max_age=3600):  # Default cache age: 1 hour
        cache_path = self.get_cache_path(url, content_type)

        if os.path.exists(cache_path):
            # Check if cache is still valid
            modified_time = os.path.getmtime(cache_path)
            if (datetime.datetime.now().timestamp() - modified_time) < max_age:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                return cache_data.get('response'), cache_data.get('headers')
        return None, None

    def set(self, url, response, headers, content_type=None):
        cache_path = self.get_cache_path(url, content_type)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump({
                'response': response,
                'headers': headers
            }, f) 