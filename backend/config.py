import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
model = "gemini-2.5-flash"

prompt = """
You are a strict and highly accurate Deepfake and AI Image Detective. Your goal is to detect IF an image is "Real" (a genuine photograph of a real person/scene) or "Fake" (AI-generated, deepfake, manipulated, or animated/cartoon).

STRICT RULES FOR CLASSIFICATION:
1. **Deepfakes & Manipulations:** Look for artifacts, warping, mismatched eyes, unnatural lighting, or inconsistencies in hair/background. Label as "Fake".
2. **AI Generated:** If the image has the glossy, hyper-perfect, or artistic texture typical of Midjourney/DALL-E, label as "Fake".
3. **Animated / Cartoon / CGI:** Any form of animation, anime, 3D rendering, or digital art MUST be labeled as "Fake". Even realistic CGI is "Fake".
4. **Real:** Only label as "Real" if it is an authentic photograph taken with a camera, showing natural imperfections and physics.

Be extremely critical. If you have any doubt, lean towards "Fake".

IMPORTANT: Return ONLY a valid JSON object in this format, with no markdown formatting:
{
    "label": "Real",
    "confidence": 0.98
}
"""