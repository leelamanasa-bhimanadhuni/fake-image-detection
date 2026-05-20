import os
import io
import base64
import json
import time
import requests
from config import prompt, key, url, model
from flask import Flask, request, jsonify, render_template
from PIL import Image

# Initialize Flask App
app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read and process image
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.thumbnail((512, 512))

        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Prepare Gemini request
        headers = {"Content-Type": "application/json"}

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        }

        # Call Gemini API with retry
        print("Sending request to Gemini...")
        for attempt in range(3):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                break
            elif response.status_code in [503, 429]:
                print(f"Attempt {attempt+1} failed with {response.status_code}, retrying...")
                time.sleep(3)
            else:
                print(f"API Error: {response.text}")
                return jsonify({'error': f'API Error: {response.status_code}'}), 500
        else:
            return jsonify({'error': 'Server busy, please try again in a moment.'}), 503

        result = response.json()

        # Parse Gemini response
        content_str = result['candidates'][0]['content']['parts'][0]['text']
        content_str = content_str.replace('```json', '').replace('```', '').strip()

        data = json.loads(content_str)
        label = data.get('label', 'Unknown')
        confidence = float(data.get('confidence', 0.5))

        return jsonify({
            'label': label,
            'confidence': f"{confidence:.2%}"
        })

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)