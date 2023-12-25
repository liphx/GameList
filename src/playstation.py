from common import *
from psnawp_api import PSNAWP
import sys

psnawp = PSNAWP(sys.argv[1])
client = psnawp.me()


def fetch(fetch_all=True, only_perfect=False, only_platinum=False):
    output = {}
    trophy_summary = client.trophy_summary()
    summary = {}
    summary['level'] = trophy_summary.trophy_level
    summary['bronze'] = trophy_summary.earned_trophies.bronze
    summary['silver'] = trophy_summary.earned_trophies.silver
    summary['gold'] = trophy_summary.earned_trophies.gold
    summary['platinum'] = trophy_summary.earned_trophies.platinum
    output['summary'] = summary
    trophies = []
    for trophy_title in client.trophy_titles():
        trophy = {}
        trophy['name'] = trophy_title.title_name
        trophy['platform'] = [i.name for i in trophy_title.title_platform]
        is_perfect = trophy_title.progress == 100
        is_platinum = trophy_title.defined_trophies.platinum > 0
        trophy['progress'] = trophy_title.progress
        trophy['bronze'] = f'{trophy_title.earned_trophies.bronze}/{trophy_title.defined_trophies.bronze}'
        trophy['silver'] = f'{trophy_title.earned_trophies.silver}/{trophy_title.defined_trophies.silver}'
        trophy['gold'] = f'{trophy_title.earned_trophies.gold}/{trophy_title.defined_trophies.gold}'
        trophy['platinum'] = f'{trophy_title.earned_trophies.platinum}/{trophy_title.defined_trophies.platinum}'
        trophy['update_time'] = format_datetime(
            trophy_title.last_updated_date_time.astimezone())
        if fetch_all or (only_perfect and is_perfect) or (only_platinum and is_platinum):
            trophies.append(trophy)
    trophies.sort(reverse=True, key=lambda trophy: (
        trophy['progress'], trophy['update_time']))
    for trophy in trophies:
        trophy['progress'] = f"{trophy['progress']}%"
    output['trophy'] = trophies
    jprint(output)


fetch()
# fetch(False, True)
