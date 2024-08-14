#!/usr/bin/env python3

import requests
import time
from functools import wraps

# Global cache dictionary
cache = {}
access_counts = {}

def cache_decorator(func):
    @wraps(func)
    def wrapper(url: str) -> str:
        global cache, access_counts
        
        # Increment access count
        access_counts[url] = access_counts.get(url, 0) + 1
        
        # Check if URL is in cache and not expired
        now = time.time()
        if url in cache and now - cache[url]['timestamp'] < 10:
            print(f"Returning cached content for {url}")
            return cache[url]['content']
        
        # Fetch page content
        print(f"Fetching content for {url}")
        content = func(url)
        
        # Update cache with fetched content and current timestamp
        cache[url] = {'content': content, 'timestamp': now}
        
        return content
    
    return wrapper

@cache_decorator
def get_page(url: str) -> str:
    """Fetches the HTML content of a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
    return response.text
