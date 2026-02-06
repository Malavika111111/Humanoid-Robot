from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# ---------- UTIL ----------
def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------- ROUTES ----------
@app.route("/")
def home():
    guest = load_json("current_guest.json")
    return render_template("index.html", guest=guest.get("name", ""))

@app.route("/person_detected", methods=["POST"])
def person_detected():
    visitors = load_json("visitors.json")
    visitors.append({"time": str(datetime.now())})
    save_json("visitors.json", visitors)
    return jsonify({"status": "ok"})

@app.route("/admin/name", methods=["POST"])
def set_name():
    name = request.json.get("name", "")
    save_json("current_guest.json", {"name": name})
    return jsonify({"status": "saved"})

@app.route("/departments")
def departments():
    data = load_json("departments.json")
    return jsonify(data)

@app.route("/department/<dept>")
def department(dept):
    data = load_json("departments.json")
    return render_template("department.html", dept=data[dept], name=dept)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
