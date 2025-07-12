from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

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

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    event_type = request.headers.get("X-GitHub-Event")
    author = "unknown"
    action = ""
    branch = ""

    if event_type == "push":
        author = data.get("pusher", {}).get("name", "unknown")
        branch = data.get("ref", "").split("/")[-1]
        action = f"pushed to {branch}"

    elif event_type == "pull_request":
        author = data.get("pull_request", {}).get("user", {}).get("login", "unknown")
        branch = data.get("pull_request", {}).get("base", {}).get("ref", "main")
        pr_action = data.get("action", "")
        if pr_action == "opened":
            action = f"created a pull request to {branch}"
        elif pr_action == "closed" and data["pull_request"].get("merged", False):
            action = f"merged a pull request to {branch}"
        else:
            return "Ignored", 200  # ignore other PR events

    else:
        return "Event not handled", 200

    now = datetime.utcnow() + timedelta(hours=5, minutes=30)  # IST
    formatted_time = now.strftime("%d %B %Y - %I:%M %p UTC")

    collection.insert_one({
        "author": author,
        "action": action,
        "timestamp": formatted_time
    })

    return "Webhook received", 200

if __name__ == "__main__":
    app.run(debug=True)