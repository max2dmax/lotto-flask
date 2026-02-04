# app.py
from flask import Flask, render_template, request
from lotto_engine_decrepatated import LottoEngine

app = Flask(__name__)

# Engine is reusable + importable
engine = LottoEngine(normal_ball_max=69, normal_ball_count=5, power_ball_max=26)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def generate():
    first = request.form.get("first_name", "")
    last = request.form.get("last_name", "")
    payload = request.form.get("payload", "")

    result = engine.generate(first, last, payload)

    return render_template(
        "result.html",
        first=first,
        last=last,
        payload=payload,
        seed_preview=result["seed_preview"],
        numbers=result["numbers"],
        powerball=result["powerball"],
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)