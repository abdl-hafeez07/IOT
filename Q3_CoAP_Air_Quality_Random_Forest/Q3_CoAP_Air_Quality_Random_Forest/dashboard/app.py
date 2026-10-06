from pathlib import Path
import asyncio
import json

from flask import Flask, jsonify, render_template

import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from coap.coap_client import get_air_quality
from model.model_utils import load_model, predict_category

app = Flask(__name__)

MODEL = None


def get_model():
    global MODEL
    if MODEL is None:
        MODEL = load_model()
    return MODEL


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/live")
def live():
    try:
        # Dashboard -> CoAP Client -> CoAP Server -> Open-Meteo
        data = asyncio.run(get_air_quality())

        model = get_model()
        category = predict_category(model, data)

        data["prediction"] = category
        data["status"] = "success"

        return jsonify(data)

    except Exception as exc:
        return jsonify({
            "status": "error",
            "error": str(exc)
        }), 500


if __name__ == "__main__":
    print("Dashboard: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
