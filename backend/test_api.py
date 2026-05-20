
import requests
import os
import sys

def test_prediction():
    url = "http://127.0.0.1:5000/predict"
    # Use a known image path associated with 'real' or 'fake'
    # Based on Find output: e:/image_detection/image_detection_data/test/real/00114.jpg
    image_path = os.path.join(os.path.dirname(__file__), '../image_detection_data/test/real/real_00114.jpg')
    
    # Correcting filename based on find output which was 'real\00114.jpg' relative to test dir
    # wait, the find output was "real\00114.jpg".
    # constructing path:
    base_data = os.path.join(os.path.dirname(__file__), '../image_detection_data/test/real')
    # Let's find a file that exists or just pick the first one from os.listdir if possible, 
    # but I can't do that easily inside this isolated script without running it. 
    # I'll rely on the find output I saw earlier: "real\00114.jpg" 
    # Be careful with the path name 'real_00114.jpg' vs '00114.jpg'. 
    # The find output showed "real\00114.jpg" inside "test" directory.
    # Ah, the find output was "real\00114.jpg" which means the file is "00114.jpg" inside "real" folder.
    
    image_path = os.path.join(base_data, '00114.jpg')
    
    if not os.path.exists(image_path):
        # Fallback to finding any file
        try:
            files = os.listdir(base_data)
            if files:
                image_path = os.path.join(base_data, files[0])
            else:
                print("No images found for testing.")
                return
        except Exception as e:
            print(f"Error accessing test data: {e}")
            return

    print(f"Testing with image: {image_path}")
    
    try:
        with open(image_path, 'rb') as img:
            files = {'file': img}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            print("Success! Response:")
            print(response.json())
        else:
            print(f"Failed. Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_prediction()
