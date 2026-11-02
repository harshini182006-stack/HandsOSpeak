
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "Hands O Speak Backend is running!"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "project": "Hands O Speak"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
