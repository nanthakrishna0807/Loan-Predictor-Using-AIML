import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import LoanPredictorEngine
from train_model import train_and_evaluate_models

app = Flask(__name__)
CORS(app)

predictor = LoanPredictorEngine()

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "service": "AI Loan Predictor ML Service",
        "status": "Online",
        "model_loaded": predictor.artifacts is not None,
        "active_model": predictor.artifacts.get("best_model_name", "None") if predictor.artifacts else "None"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No input payload provided"}), 400

        result = predictor.predict(data)
        return jsonify({
            "success": True,
            "prediction": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/model-info", methods=["GET"])
def get_model_info():
    if os.path.exists("model_meta.json"):
        with open("model_meta.json", "r") as f:
            meta = json.load(f)
        return jsonify({"success": True, "metadata": meta})
    else:
        return jsonify({"success": False, "message": "Model metadata not found"}), 444

@app.route("/accuracy", methods=["GET"])
def get_accuracy():
    if os.path.exists("model_meta.json"):
        with open("model_meta.json", "r") as f:
            meta = json.load(f)
        return jsonify({
            "success": True,
            "best_model": meta.get("best_model"),
            "best_accuracy": meta.get("best_accuracy"),
            "comparison": meta.get("comparison")
        })
    return jsonify({"success": False, "accuracy": "N/A"})

@app.route("/retrain", methods=["POST"])
def retrain():
    try:
        meta = train_and_evaluate_models("dataset.csv")
        # Reload predictor engine
        global predictor
        predictor = LoanPredictorEngine()
        return jsonify({
            "success": True,
            "message": "Model retrained successfully!",
            "metadata": meta
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("Starting ML Flask API Service on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=False)
