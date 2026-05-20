
import requests
import os
import time
import sys

def test_prediction_loop():
    url = "http://127.0.0.1:5000/predict"
    base_data = os.path.join(os.path.dirname(__file__), '../image_detection_data/test/real')
    image_path = os.path.join(base_data, '00114.jpg')
    
    if not os.path.exists(image_path):
        print("Image not found path.")
        return

    print("Waiting for server...")
    for i in range(30):
        try:
            requests.get("http://127.0.0.1:5000/")
            print("Server is up!")
            break
        except:
            time.sleep(2)
            sys.stdout.write(".")
            sys.stdout.flush()
    else:
        print("\nServer timed out.")
        return

    print(f"\nTesting with image: {image_path}")
    try:
        with open(image_path, 'rb') as img:
            files = {'file': img}
            response = requests.post(url, files=files)
            
        print("Response Code:", response.status_code)
        print("Response Body:", response.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_prediction_loop()
