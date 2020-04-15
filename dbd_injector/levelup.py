import requests
import json

with open("session.json", "r") as file:
    bhvrSession = json.load(file)["bhvrSession"]

for i in range(0, 10000000):
    response = requests.post(
        "https://latest.live.dbd.bhvronline.com/api/v1/extensions/playerLevels/earnPlayerXp",
        json={
            "data": {
                "consecutiveMatch": 1,
                "emblemQualities": [
                    "Iridescent",
                    "Iridescent",
                    "Iridescent",
                    "Iridescent"
                ],
                "isFirstMatch": True,
                "levelVersion": i,
                "matchTime": 1000,
                "platformVersion": "steam",
                "playerType": "survivor"
            }
        },
        headers={
            "Accept-Encoding": "deflate, gzip",
            "Accept": "*/*",
            "Content-Type": "application/json",
        },
        cookies={
            "bhvrSession": bhvrSession
        }).json()
    print(response)