from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
collection = db["events"]

@app.route("/")
def home():
    return "Webhook server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    # Get event type from headers
    github_event = request.headers.get("X-GitHub-Event", "")
    author = ""
    action = ""
    from_branch = ""
    to_branch = ""

    if github_event == "push":
        action = "PUSH"
        author = data.get("pusher", {}).get("name", "unknown")
        to_branch = data.get("ref", "").split("/")[-1]

    elif github_event == "pull_request":
        pr_action = data.get("action", "").lower()
        if pr_action == "opened":
            action = "PULL_REQUEST"
        elif pr_action == "closed" and data.get("pull_request", {}).get("merged", False):
            action = "MERGE"
        else:
            return "Event not handled", 200

        author = data.get("pull_request", {}).get("user", {}).get("login", "unknown")
        from_branch = data.get("pull_request", {}).get("head", {}).get("ref", "")
        to_branch = data.get("pull_request", {}).get("base", {}).get("ref", "")

    else:
        return "Event not handled", 200

    # Skip saving if author is unknown
    if not author or author == "unknown":
        return "Invalid data", 400

    timestamp = datetime.utcnow().isoformat() + "Z"

    # Insert into MongoDB
    collection.insert_one({
        "author": author,
        "action": action,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    })

    print("Saved event:", action, author, to_branch)
    return "webhook received", 200

if __name__ == "__main__":
    app.run(debug=True)
