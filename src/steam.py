from common import *
import requests
import sys
import time


# https://developer.valvesoftware.com/wiki/Steam_Web_API
# https://wiki.teamfortress.com/wiki/User:RJackson/StorefrontAPI
class SteamAPI:
    def __init__(self, key, steamid):
        self.key = key
        self.steamid = steamid
        self.session = requests.Session()
        self.requests_count = 0

    def __del__(self):
        eprint('requests_count:', self.requests_count)

    def fetch(self, url, try_times=5, sleep_interval=1):
        if try_times == 0:
            return None
        try:
            self.requests_count += 1
            return self.session.get(url)
        except Exception:
            time.sleep(sleep_interval)
            return self.fetch(url, try_times=try_times - 1, sleep_interval=sleep_interval)

    def GetOwnedGames(self, steamid=None):
        if steamid is None:
            steamid = self.steamid
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={
            steamid}&format=json&skip_unvetted_apps=0&include_appinfo=1&include_played_free_games=1&include_free_sub=0'
        r = self.fetch(url)
        return r.json()

    def GetGlobalAchievementPercentagesForApp(self, appid):
        url = f'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={
            appid}'
        r = self.fetch(url)
        return r.json()

    def GetPlayerAchievements(self, appid, language='english'):
        url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={
            appid}&key={self.key}&steamid={self.steamid}&l={language}'
        r = self.fetch(url)
        return r.json()

    def GetPlayerSummaries(self):
        url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={
            self.key}&steamids={self.steamid}'
        r = self.fetch(url)
        return r.json()

    def GetFriendList(self):
        url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={
            self.key}&steamid={self.steamid}&relationship=friend'
        r = self.fetch(url)
        return r.json()

    def GetUserStatsForGame(self, appid):
        url = f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={
            appid}&key={self.key}&steamid={self.steamid}'
        r = self.fetch(url)
        return r.json()

    def GetRecentlyPlayedGames(self):
        url = f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={
            self.key}&steamid={self.steamid}&format=json'
        r = self.fetch(url)
        return r.json()

    def GetAppDetails(self, appid):
        url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
        return self.fetch(url).json()


def GetAppAchievement(key, steamid, appid):
    api = SteamAPI(key, steamid)
    achievements = api.GetPlayerAchievements(appid)
    achievements_schinese = api.GetPlayerAchievements(appid, 'schinese')
    achievements_global_percentages = api.GetGlobalAchievementPercentagesForApp(
        appid)
    gamename = achievements['playerstats']['gameName']
    # jprint(achievements)
    # jprint(achievements_schinese)
    # jprint(achievements_global_percentages)

    output = {}

    all_games = api.GetOwnedGames()
    output['all_games'] = all_games

    details = api.GetAppDetails(appid)
    output['details'] = details

    output['achievements'] = []
    for i, achievement in enumerate(achievements['playerstats']['achievements']):
        achievement_chinese = achievements_schinese['playerstats']['achievements'][i]
        achievement_global_percentages = achievements_global_percentages[
            'achievementpercentages']['achievements'][i]
        item = {}
        item['name'] = achievement['name']
        item['description'] = achievement['description']
        item['chinese_name'] = achievement_chinese['name']
        item['chinese_description'] = achievement_chinese['description']
        item['achieved'] = achievement['achieved']
        if item['achieved'] == 1:
            item['unlocktime'] = format_time(achievement['unlocktime'])
        item['global_percentage'] = achievement_global_percentages['percent']
        output['achievements'].append(item)
    jprint(output)


def main(key, steamid):
    api = SteamAPI(key, steamid)
    output = []
    games = api.GetOwnedGames()['response']
    for game in games['games']:
        appid = str(game['appid'])
        item = {}
        item['appid'] = appid
        achievements = api.GetPlayerAchievements(appid)['playerstats']
        if ('error' in achievements):
            details = api.GetAppDetails(appid)
            if details[appid]['success']:
                item['name'] = details[appid]['data']['name']
                output.append(item)
            continue
        item['name'] = achievements['gameName']
        if 'rtime_last_played' in game and game['rtime_last_played'] != 0:
            item['last_time'] = format_time(game['rtime_last_played'])
        item['total_time'] = game['playtime_forever']
        output.append(item)
    jprint(output)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
