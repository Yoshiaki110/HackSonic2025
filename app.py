from flask import Flask, request, render_template, jsonify, Response
import base64
import os
import json

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json
    image_data = data['image']
    image_data = image_data.split(",")[1]  # remove the data URL header
    image_bytes = base64.b64decode(image_data)

    file_path = os.path.join(UPLOAD_FOLDER, 'captured_image.png')
    with open(file_path, 'wb') as f:
        f.write(image_bytes)

    return jsonify({'message': '画像が保存されました'}), 200 

if __name__ == '__main__':
    app.run(debug=True)
