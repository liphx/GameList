from common import *
import sys

headers['Cookie'] = sys.argv[1]
refund = set()
purchase = set()


def fetch(url, zh):
    if zh:
        url = url + '&locale=zh-Hans'
    r = fetch_url(url)
    if r is None:
        return
    data = r.json()
    for order in data['orders']:
        for item in order['items']:
            description = ' '.join(item['description'].replace(
                '《', ' ').replace('》', ' ').split())
            if order['orderType'] == 'REFUND':
                refund.add(description)
            elif order['orderType'] == 'PURCHASE' and description not in refund:
                purchase.add(description)
    nextPageToken = data['nextPageToken']
    if not nextPageToken:
        return
    url = f'https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?sortDir=DESC&sortBy=DATE&nextPageToken={nextPageToken}'
    fetch(url, zh)


url = 'https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?sortDir=DESC&sortBy=DATE'
# fetch(url, False)
fetch(url, True)
jprint(sorted(list(purchase)))
