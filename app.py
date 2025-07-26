from flask import Flask, render_template, request
from google.cloud import firestore, storage
from datetime import datetime
import os

app = Flask(__name__)
db = firestore.Client()

# ✅ Cloud Storage Upload Function
def upload_to_bucket(data):
    bucket_name = "gcp_pushpesh"  # Replace with your actual bucket name
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Unique filename with timestamp
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"contact_submissions/form_{now}.txt"
    blob = bucket.blob(file_name)

    content = f"Name: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}\n"
    blob.upload_from_string(content)
    print(f"Uploaded to bucket: {file_name}")

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

    db.collection('contacts').add(data)     # Save to Firestore
    upload_to_bucket(data)                  # Also save to Cloud Storage

    return "Thanks! Your message has been received."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run uses this
    app.run(host='0.0.0.0', port=port, debug=False)
