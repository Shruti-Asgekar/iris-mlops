import os
import time
import joblib
from flask import Flask, render_template, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
SPECIES = ["setosa", "versicolor", "virginica"]
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

# ---- Monitoring metrics (scraped by Prometheus at /metrics) ----
REQUESTS = Counter("app_requests_total", "Total HTTP requests", ["endpoint"])
PREDICTIONS = Counter("app_predictions_total", "Predictions by species", ["species"])
ERRORS = Counter("app_errors_total", "Invalid prediction requests")
LATENCY = Histogram("app_prediction_latency_seconds", "Prediction latency")


@app.route("/")
def home():
    REQUESTS.labels("/").inc()
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/predict", methods=["POST"])
def predict():
    REQUESTS.labels("/predict").inc()
    start = time.time()
    data = request.get_json(silent=True) or request.form
    try:
        feats = [float(data[k]) for k in
                 ("sepal_length", "sepal_width", "petal_length", "petal_width")]
    except (KeyError, ValueError, TypeError):
        ERRORS.inc()
        return jsonify(error="Provide 4 numeric features"), 400
    species = SPECIES[int(model.predict([feats])[0])]
    PREDICTIONS.labels(species).inc()
    LATENCY.observe(time.time() - start)
    return jsonify(species=species)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
