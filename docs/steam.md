# Steam

```shell
python3 src/steam.py key steamid > steam.json
```

- key：[注册 Steam Web API 密钥](https://steamcommunity.com/dev/apikey)。
- steamid：Steam ID，非用户名，例如[profiles](https://steamcommunity.com/profiles/76561198373797938/)后面的数字。

输出格式如下

```json
[
    {
        "appid": 550,
        "name": "Left 4 Dead 2",
        "last_time": "2020-07-12 20:50:10",
        "total_time": 994
    },
    {
        "appid": 8870,
        "name": "BioShock Infinite",
        "total_time": 0
    },
    {
        "appid": 730,
        "name": "Counter-Strike 2",
        "last_time": "2023-06-16 00:30:21",
        "total_time": 20700
    }
]
```

- appid：Steam中的游戏ID。
- last_time：上次游玩的时间。
- total_time：游戏总时间，单位是分钟。

参考链接

- [Steam 社区 :: Steam Web API 文档](https://steamcommunity.com/dev)
- [Steam Web API - Valve Developer Community](https://developer.valvesoftware.com/wiki/Steam_Web_API)
