from websocket import WebSocketApp
import cv2
import numpy as np
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def process_frame(frame_data):
    try:
        # Decode the binary data into an image
        np_arr = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Convert BGR image to RGB as YOLO expects RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None

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