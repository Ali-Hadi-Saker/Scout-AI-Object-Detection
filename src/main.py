from websocket import WebSocketApp
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def connect_to_websocket():
    ws = WebSocketApp("ws://localhost:8080")
    ws.run_forever()

if __name__ == "__main__":
    connect_to_websocket()