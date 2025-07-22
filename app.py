from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    input_text = data.get("text")

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"generate html for this:\n\n{input_text}"

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return jsonify({"summary": result.get("response", "").strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
