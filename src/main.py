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

        results = model(rgb_frame)
        detections = []
        for det in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = det[:6]
            label = results.names[int(cls)]
            location = (int(x1), int(y1), int(x2), int(y2))
            detections.append({"label": label}, {"location": location})

            print(f"Detections: {detections}") 
        return detections
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None

def on_message(ws, message):
    try:
        print("Received frame from WebSocket server")
        processed_data = process_frame(message)
        if processed_data:
            # Convert detections to string format for sending
            processed_data_str = str(processed_data).encode('utf-8')
            # Send the processed data back to the server
            print("Sent processed data back to server")
            # Send as binary with opcode=0x2
            ws.send(processed_data_str, opcode=0x2)  
            print(processed_data_str)
        else:
            print("No processed data to send")
            
    except Exception as e:
        print(f"Error in message handling: {e}")



        
def connect_to_websocket():
    ws = WebSocketApp("ws://localhost:8080",
                    on_message=on_message,)
    ws.run_forever()

if __name__ == "__main__":
    connect_to_websocket()