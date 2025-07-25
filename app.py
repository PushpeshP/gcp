from flask import Flask, render_template, request
from google.cloud import firestore
import os
from datetime import datetime


app = Flask(__name__)
def upload_to_bucket(data):
    bucket_name = "gcp_pushpesh"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Unique file name with timestamp
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"contact_submissions/form_{now}.txt"
    blob = bucket.blob(file_name)

    content = f"Name: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}\n"
    blob.upload_from_string(content)
    print(f"Uploaded to bucket: {file_name}")

db = firestore.Client()

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "message": request.form['message']
    }

    db.collection('contacts').add(data)     # 🔹 Firestore में store
    upload_to_bucket(data)                  # 🔹 Cloud Storage में .txt file भेजो

    return "Thanks! Your message has been received."
