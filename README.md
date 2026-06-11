**🔍 FIDAC — Fake Image Detection using AI/ML**

A deep learning-based web application that detects fake/manipulated images using DenseNet121 transfer learning. Built as a final-year capstone project, achieving 95–97% accuracy on a dataset of 140,000+ images.

**📌 Project Overview**

FIDAC (Fake Image Detection using AI/ML) addresses the growing problem of deepfakes and manipulated media. The model classifies images as real or fake using transfer learning on DenseNet121, deployed via a Flask web interface.

## 🚀 Live Demo
Upload any image and get instant Real/Fake classification with confidence score.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **AI Model:** DenseNet121 (Transfer Learning, TensorFlow/Keras)
- **Vision API:** Google Gemini 2.5 Flash
- **Frontend:** HTML, CSS, JavaScript
- **Framework**: TensorFlow / Keras
- **Dataset:** Real and Fake Face Detection Dataset
- 

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
