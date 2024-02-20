from common import *
import sys


class SteamAPI:
    def __init__(self, key, steamid):
        self.key = key
        self.steamid = steamid

    def GetOwnedGames(self):
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={self.steamid}&format=json'
        r = fetch_url(url)
        return r.json()

    def GetPlayerAchievements(self, appid):
        url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={self.key}&steamid={self.steamid}'
        r = fetch_url(url)
        return r.json()

    def GetPlayerSummaries(self):
        url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.key}&steamids={self.steamid}'
        r = fetch_url(url)
        return r.json()

    def GetFriendList(self):
        url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.key}&steamid={self.steamid}&relationship=friend'
        r = fetch_url(url)
        return r.json()

    def GetUserStatsForGame(self, appid):
        url = f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={self.key}&steamid={self.steamid}'
        r = fetch_url(url)
        return r.json()

    def GetRecentlyPlayedGames(self):
        url = f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={self.key}&steamid={self.steamid}&format=json'
        r = fetch_url(url)
        return r.json()


def main(key, steamid):
    api = SteamAPI(key, steamid)
    # jprint(api.GetPlayerSummaries())
    # jprint(api.GetFriendList())
    # jprint(api.GetRecentlyPlayedGames())

    output = []
    games = api.GetOwnedGames()['response']
    for game in games['games']:
        item = {}
        item['appid'] = game['appid']
        Achievements = api.GetPlayerAchievements(game['appid'])['playerstats']
        if ('error' in Achievements):
            output.append(item)
            continue
        item['name'] = Achievements['gameName']
        if 'rtime_last_played' in game and game['rtime_last_played'] != 0:
            item['last_time'] = format_time(game['rtime_last_played'])
        item['total_time'] = game['playtime_forever']
        output.append(item)
    jprint(output)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
