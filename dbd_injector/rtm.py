import json
import websocket

def on_message(ws, message):
    print(message)

url = json.loads(open("rtm.json", "r").read())["url"]
ws = websocket.WebSocketApp(url, on_message=on_message)
ws.run_forever()