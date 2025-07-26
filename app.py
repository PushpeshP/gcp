from flask import Flask, render_template, request
from google.cloud import firestore, storage, pubsub_v1
from datetime import datetime
import os, json

app = Flask(__name__)
db = firestore.Client()

def upload_to_bucket(data):
    bucket_name = "gcp_pushpesh"  # ✅ Your actual bucket name
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"contact_submissions/form_{now}.txt"
    blob = bucket.blob(file_name)

    content = f"Name: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}\n"
    blob.upload_from_string(content)
    print(f"✅ Uploaded to Cloud Storage: {file_name}")

def publish_to_pubsub(data):
    publisher = pubsub_v1.PublisherClient()
    
    # ✅ Dynamic project and topic from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_id = os.getenv("PUBSUB_TOPIC", "cloud-build-topics")  # default fallback
    topic_path = publisher.topic_path(project_id, topic_id)

    message_json = json.dumps(data).encode("utf-8")
    future = publisher.publish(topic_path, data=message_json)
    print(f"✅ Pub/Sub message published to {topic_id}: {future.result()}")

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "message": request.form['message']
    }

    db.collection('contacts').add(data)
    upload_to_bucket(data)
    publish_to_pubsub(data)

    return "✅ Thanks! Your message has been received."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
