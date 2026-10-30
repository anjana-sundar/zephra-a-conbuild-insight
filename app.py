from pathlib import Path
from uuid import uuid4

import cv2
from flask import Flask, render_template, request, send_from_directory, url_for
from ultralytics import YOLO
from werkzeug.utils import secure_filename

from tender_risk import DEMO_EXAMPLES, assess_tender_risk, parse_tender_inputs

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
RESULT_FOLDER = BASE_DIR / "results"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULT_FOLDER.mkdir(exist_ok=True)

model = YOLO(str(BASE_DIR / "models" / "best.pt"))


def render_dashboard(*, error=None, result=None, status=200):
    return (
        render_template(
            "index.html",
            error=error,
            result=result,
        ),
        status,
    )


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/bim")
def bim_twin():
    return render_template("bim.html")


@app.route("/safety", methods=["GET", "POST"])
def worker_safety():
    if request.method == "GET":
        return render_dashboard()

    image = request.files.get("image")
    if image is None or image.filename == "":
        return render_dashboard(error="Choose an image to analyze.", status=400)

    filename = secure_filename(image.filename)
    extension = Path(filename).suffix.lower().lstrip(".")
    if not filename or extension not in ALLOWED_EXTENSIONS:
        return render_dashboard(
            error="Upload a JPG, PNG, or WEBP image.", status=400
        )

    unique_name = f"{uuid4().hex}_{filename}"
    upload_path = UPLOAD_FOLDER / unique_name
    image.save(upload_path)

    prediction = model(str(upload_path), verbose=False)[0]
    detections = []
    counts = {}

    if prediction.boxes is not None:
        for box in prediction.boxes:
            class_id = int(box.cls.item())
            label = prediction.names[class_id]
            confidence = float(box.conf.item())
            detections.append(
                {"label": label, "confidence": round(confidence * 100)}
            )
            counts[label] = counts.get(label, 0) + 1

    result_name = f"{uuid4().hex}.jpg"
    result_path = RESULT_FOLDER / result_name
    if not cv2.imwrite(str(result_path), prediction.plot()):
        raise RuntimeError(f"Unable to save annotated image to {result_path}")

    return render_dashboard(
        result={
            "image_url": url_for("result_image", filename=result_name),
            "filename": filename,
            "total": len(detections),
            "counts": counts,
            "detections": detections,
        }
    )


@app.route("/tender-risk", methods=["GET", "POST"])
def tender_risk():
    assessment = None
    errors = []
    values = {}

    if request.method == "POST":
        values, errors = parse_tender_inputs(request.form)
        if not errors:
            assessment = assess_tender_risk(values)

    return (
        render_template(
            "tender_risk.html",
            assessment=assessment,
            errors=errors,
            values=values if request.method == "POST" else {},
            demo_examples=DEMO_EXAMPLES,
        ),
        400 if errors else 200,
    )


@app.route("/results/<filename>")
def result_image(filename):
    return send_from_directory(RESULT_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
