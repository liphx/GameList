from common import *
import sys

headers['Cookie'] = sys.argv[1]
output = set()


def fetch(url, zh):
    if zh:
        url = url + '&locale=zh-Hans'
    r = fetch_url(url)
    if r is None:
        return
    data = r.json()
    for order in data['orders']:
        for item in order['items']:
            description = item['description']
            if description[0] == '《' and description[-1] == '》':
                description = description[1:-1]
            if order['orderType'] == 'PURCHASE':
                output.add(description)
            elif order['orderType'] == 'REFUND' and description in output:
                output.remove(description)
    nextPageToken = data['nextPageToken']
    if not nextPageToken:
        return
    url = f'https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?sortDir=DESC&sortBy=DATE&nextPageToken={nextPageToken}'
    fetch(url, zh)


url = 'https://www.epicgames.com/account/v2/payment/ajaxGetOrderHistory?sortDir=DESC&sortBy=DATE'
fetch(url, False)
jprint(list(output))
