from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['github_events']
collection = db['events']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/events")
def get_events():
    events = []
    for event in collection.find().sort("_id", -1).limit(10):
        events.append({
            "actor": event.get("actor", "unknown"),
            "action": event.get("action", "did something"),
            "timestamp": event.get("timestamp", "unknown")
        })
    return jsonify(events)

# ✅ Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    actor = data.get("pusher", {}).get("name", "unknown")
    branch = data.get("ref", "").split("/")[-1] or "main"
    now = datetime.utcnow()
    formatted_time = now.strftime("%d %B %Y - %I:%M %p UTC")

    action = f'pushed to {branch}'
    timestamp = formatted_time

    # ✅ Insert into MongoDB
    collection.insert_one({
   "actor": actor,
    "action": action,
    "timestamp": timestamp
    })

    return "Webhook received", 200

if __name__ == "__main__":
    app.run(debug=True)