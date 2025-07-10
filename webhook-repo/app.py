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
            "from_branch": event.get("from_branch","unknown"),
            "to_branch": event.get("to_branch","unknown"),
            "timestamp": event.get("timestamp", "unknown")
        })
    return jsonify(events)

# ✅ Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    # ✅ Extract data from GitHub webhook payload
    actor = data.get("pusher", {}).get("name", "unknown")
    print("Github Webhook received!")
    print("actor:",actor)
    action = "pushed code"
    timestamp = data.get("head_commit", {}).get("timestamp", "unknown")

    # ✅ Insert into MongoDB
    collection.insert_one({
        "actor": actor,
        "action": action,
        "timestamp": timestamp
    })

    return "Webhook received", 200

if __name__ == "__main__":
    app.run(debug=True)
