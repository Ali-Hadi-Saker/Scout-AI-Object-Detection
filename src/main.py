from websocket import WebSocketApp
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def process_frame(frame_data):
    pass

def on_message(ws, message):
    try:
        print("Received frame from WebSocket server")
        process_frame(message)
    except Exception as e:
        print(f"Error in message handling: {e}")



        
def connect_to_websocket():
    ws = WebSocketApp("ws://localhost:8080",
                    on_message=on_message,)
    ws.run_forever()

if __name__ == "__main__":
    connect_to_websocket()