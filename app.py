import re # for clean AI response
import requests
from flask import Flask, request, jsonify, render_template

# Replace your api
GEMINI_API_KEY = "YOUR API"

# API URL
GEMINI_API_URL = "your API URL"



#  Initialize Flask app
app = Flask(__name__)

# Serve the Frontend
@app.route('/')
def home():
    return render_template("index.html")  # Load Chat UI

# Function to clean AI responses 
def clean_response(text):
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)  # Removes * and ** formatting
    text = re.sub(r"_+", "", text)  # Removes underscores if any
    return text.strip()

# API Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided!"}), 400

    try:
        # Prepare API request payload
        payload = {
            "contents": [{"parts": [{"text": user_message}]}]
        }

        # Send request to API
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response_data = response.json()

        #  Debugging: Print API Response in Terminal
        print("API Response:", response_data)

        # Extract and clean AI response
        if "candidates" in response_data and response_data["candidates"]:
            raw_reply = response_data["candidates"][0]["content"]["parts"][0]["text"]
            ai_reply = clean_response(raw_reply)  # Clean AI response
        else:
            ai_reply = "AI did not return a valid response."

        return jsonify({"user": user_message, "bot": ai_reply})

    except Exception as e:
        print("Flask Error:", e)  # Print error in Flask console
        return jsonify({"error": "AI service unavailable"}), 500

# Run Flask Server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
