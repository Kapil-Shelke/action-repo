from datetime import datetime, timedelta
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
            "author": event.get("author", "unknown"),
            "action": event.get("action", "did something"),
            "timestamp": event.get("timestamp", "unknown")
        })
    return jsonify(events)

# Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    action = ""
    author = ""
    branch = ""

    # PUSH event
    if "pusher" in data:
        author = data.get("pusher", {}).get("name", "unknown")
        branch = data.get("ref", "").split("/")[-1] or "main"
        action = f"pushed to {branch}"

    # PULL REQUEST CREATED
    elif data.get("action") == "opened" and "pull_request" in data:
        author = data.get("sender", {}).get("login", "unknown")
        branch = data.get("pull_request", {}).get("base", {}).get("ref", "main")
        action = f"created pull request to {branch}"

    # PULL REQUEST MERGED
    elif data.get("action") == "closed" and data.get("pull_request", {}).get("merged", False):
        author = data.get("sender", {}).get("login", "unknown")
        branch = data.get("pull_request", {}).get("base", {}).get("ref", "main")
        action = f"merged pull request to {branch}"

    # Format timestamp
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    formatted_time = now.strftime("%d %B %Y - %I:%M %p UTC")

    if action:
        collection.insert_one({
            "author": author,
            "action": action,
            "timestamp": formatted_time
        })

    return "Webhook received", 200

if __name__ == "__main__":
    app.run(debug=True)