from common import *


def fetch(user):
    url = f'https://www.gog.com/u/{user}/games/stats?sort=total_playtime&order=desc&page=1'
    r = fetch_url(url)
    if r is None:
        return
    items = r.json()['_embedded']['items']
    jprint([item['game']['title'] for item in items])


fetch('liphx')
