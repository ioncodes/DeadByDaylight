import requests
import json

with open("session.json", "r") as file:
    bhvrSession = json.load(file)["bhvrSession"]

while True:
    response = requests.put(
        "https://latest.live.dbd.bhvronline.com/api/v1/ranks/pips",
        json={
            "forceReset": True,
            "killerPips": 2,
            "survivorPips": 2
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