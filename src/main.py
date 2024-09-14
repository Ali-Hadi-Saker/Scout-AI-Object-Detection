from websocket import WebSocketApp

def connect_to_websocket():
    ws = WebSocketApp("ws://localhost:8080")
    ws.run_forever()

if __name__ == "__main__":
    connect_to_websocket()