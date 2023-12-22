__all__ = [
    'eprint',
    'lines',
    'fetch_url',
    'format_time',
]

import sys
import time
import requests
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def lines(path):
    try:
        return list(filter(lambda s: s, open(path, 'r', encoding='utf-8').read().split('\n')))
    except Exception:
        return []


def fetch_url(url, headers=headers, try_times=5, sleep_interval=1):
    if try_times == 0:
        return None
    try:
        return requests.get(url, headers=headers)
    except Exception:
        time.sleep(sleep_interval)
        return fetch_url(url, headers=headers, try_times=try_times - 1)


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
