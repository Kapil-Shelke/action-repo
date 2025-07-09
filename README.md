# 🔔 GitHub Webhook Tracker

A lightweight Flask-based project to *track GitHub push events* using *webhooks, store them in **MongoDB*, and display them in real-time on a web interface.

---

## 📌 Features

- 🛰 Receives GitHub Webhook POST events
- 🧠 Extracts important data like actor, action, and timestamp
- 💾 Stores event data in MongoDB
- 🌐 Displays latest GitHub activity on a dynamic webpage
- 🚀 Easy-to-run locally using Python & Ngrok

---
## 🛠 Tech Stack

| Technology     | Description                        |
|----------------|------------------------------------|
| Python         | Backend Language                   |
| Flask          | Web Framework                      |
| MongoDB        | NoSQL Database                     |
| Ngrok          | For public tunnel (Webhook URL)    |
| HTML/CSS/JS    | Frontend Page                      |
| GitHub Webhook | Triggering source of event         |

---

## ⚙ Setup Instructions

### 1. Clone this Repository

```bash
git clone https://github.com/Kapil-Shelke/webhook.git
cd webhook
2. Install Dependencies

pip install -r requirements.txt

3. Run Flask App

python app.py

It will start at: http://localhost:5000


---

🔗 Ngrok (Expose to Web)

ngrok http 5000

Copy the https://xxxxx.ngrok-free.app URL — this will be your Payload URL for GitHub.


---
⚙ Setup Webhook on GitHub

1. Go to your GitHub repo → Settings → Webhooks → Add Webhook


2. Payload URL: https://xxxxx.ngrok-free.app/webhook


3. Content type: application/json


4. Select: Just the push event


5. Click Add Webhook

---
🚀 Trigger Webhook

echo "webhook testing 🚀" >> test.txt
git add .
git commit -m "Trigger Webhook"
git push


---

📊 Output

Flask Terminal:

Github Webhook received!
actor: Kapil-Shelke
action: pushed to main

MongoDB Compass:

{
  actor: "Kapil-Shelke",
  action: "pushed to main",
  timestamp: "2025-07-09T17:30:00Z"
}


---

🙌 Author

Kapil Nilkanth Shelke

🔗 GitHub

📧 shelke.kapil224@gmail.com



---

⭐ Star this repo if you found it helpful!

---
