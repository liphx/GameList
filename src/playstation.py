from common import *
from psnawp_api import PSNAWP
import sys

psnawp = PSNAWP(sys.argv[1])
client = psnawp.me()


def fetch(fetch_all=True, only_perfect=False, only_platinum=False):
    trophy_summary = client.trophy_summary()
    summary = {}
    summary['level'] = trophy_summary.trophy_level
    summary['game'] = 0
    summary['total'] = trophy_summary.earned_trophies.bronze + trophy_summary.earned_trophies.silver + \
        trophy_summary.earned_trophies.gold + trophy_summary.earned_trophies.platinum
    summary['bronze'] = trophy_summary.earned_trophies.bronze
    summary['silver'] = trophy_summary.earned_trophies.silver
    summary['gold'] = trophy_summary.earned_trophies.gold
    summary['platinum'] = trophy_summary.earned_trophies.platinum
    summary['perfect'] = 0
    trophies = []
    perfect = []
    platinum = []
    for trophy_title in client.trophy_titles():
        summary['game'] += 1
        trophy = {}
        trophy['name'] = trophy_title.title_name.strip()
        trophy['platform'] = ','.join(
            sorted([i.name for i in trophy_title.title_platform]))
        is_perfect = trophy_title.progress == 100
        if is_perfect:
            summary['perfect'] += 1
            perfect.append(f'{trophy["name"]} ({trophy["platform"]})')
        is_platinum = trophy_title.earned_trophies.platinum > 0
        if is_platinum:
            platinum.append(f'{trophy["name"]} ({trophy["platform"]})')
        trophy['progress'] = trophy_title.progress
        if trophy_title.defined_trophies.bronze > 0:
            trophy['bronze'] = f'{trophy_title.earned_trophies.bronze}/{trophy_title.defined_trophies.bronze}'
        if trophy_title.defined_trophies.silver > 0:
            trophy['silver'] = f'{trophy_title.earned_trophies.silver}/{trophy_title.defined_trophies.silver}'
        if trophy_title.defined_trophies.gold > 0:
            trophy['gold'] = f'{trophy_title.earned_trophies.gold}/{trophy_title.defined_trophies.gold}'
        if trophy_title.defined_trophies.platinum > 0:
            trophy['platinum'] = f'{trophy_title.earned_trophies.platinum}/{trophy_title.defined_trophies.platinum}'
        trophy['update_time'] = format_datetime(
            trophy_title.last_updated_date_time.astimezone())
        if fetch_all or (only_perfect and is_perfect) or (only_platinum and is_platinum):
            trophies.append(trophy)
    # trophies.sort(reverse=True, key=lambda trophy: (trophy['progress'], trophy['update_time']))
    trophies.sort(reverse=True, key=lambda trophy: (trophy['update_time']))
    for trophy in trophies:
        trophy['progress'] = f"{trophy['progress']}%"
    output = {}
    output['summary'] = summary
    output['trophy'] = trophies
    output['platinum'] = platinum
    output['perfect'] = perfect
    jprint(output)


fetch()
