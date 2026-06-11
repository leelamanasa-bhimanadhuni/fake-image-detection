# 🔍 Fake Image Detection using AI

A web application that detects whether an image is **Real** or **Fake** (AI-generated, deepfake, or manipulated) using Google Gemini 2.5 Flash Vision API and a DenseNet121 CNN model.

## 🚀 Live Demo
Upload any image and get instant Real/Fake classification with confidence score.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **AI Model:** DenseNet121 (Transfer Learning, TensorFlow/Keras)
- **Vision API:** Google Gemini 2.5 Flash
- **Frontend:** HTML, CSS, JavaScript
- **Dataset:** Real and Fake Face Detection Dataset

## ✨ Features
- Drag & Drop image upload
- Real/Fake classification with confidence score
- Auto-retry on API errors


## 📁 Project Structure

fake-image-detection/

├── backend/

│   ├── app.py        # Flask API

│   ├── config.py     # Configuration

│   └── train.py      # Model training

├── templates/

│   └── index.html    # Frontend UI

├── static/

│   ├── style.css

│   └── script.js

└── requirements.txt
