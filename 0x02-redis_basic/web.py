#!/usr/bin/env python3

import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()

def data_cacher(method: Callable) -> Callable:
    @wraps(method)
    def invoker(url) -> str:
        # Increment count as a string
        redis_store.incr(f'count:{url}')
        
        # Attempt to get result from cache
        result = redis_store.get(f'result:{url}')
        if result:
            # Decode bytes to string
            return result.decode('utf-8')
        
        # If not in cache, fetch using the method
        result = method(url)
        
        # Store count as '0' (string) and set result with expiration
        redis_store.set(f'count:{url}', '0')
        redis_store.setex(f'result:{url}', 10, result.encode('utf-8'))  # Encode string to bytes
        
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    return requests.get(url).text