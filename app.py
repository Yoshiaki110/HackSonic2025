from flask import Flask, request, jsonify, render_template, send_from_directory
import base64
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return 'OK'

@app.route('/pub')
def pub():
    return render_template('pub.html')

@app.route('/sub')
def sub():
    return render_template('sub.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data['image']

    # 画像データのBase64部分を取り出してデコード
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    # 画像を保存
    image = Image.open(BytesIO(image_bytes))
    image.save('overlay_image.png')

    return jsonify({'message': 'Image received successfully'})

if __name__ == '__main__':
    app.run(debug=True)
