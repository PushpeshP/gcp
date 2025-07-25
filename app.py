from flask import Flask, render_template, request
from google.cloud import firestore
import os

app = Flask(__name__)
db = firestore.Client()

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
    return "Thanks! Your message has been received."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  #Cloud Run uses env PORT
    app.run(host='0.0.0.0', port=port, debug=Fals