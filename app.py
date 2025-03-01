from flask import Flask, request, jsonify, render_template, send_from_directory
import base64
from PIL import Image
from io import BytesIO
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return 'OK'

@app.route('/', methods=['POST'])
def upload_file():
    for file_key in request.files:
        file = request.files[file_key]
        #file_name = file.filename
        file_name = UPLOAD_FOLDER + '/scan.jpg'
        try:
            file.save(file_name)
            return '', 200
        except Exception as e:
            return '', 500
            break

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
    fname = UPLOAD_FOLDER + '/' + str(uuid.uuid4()) + '.png'
    image.save(fname)

    return jsonify({'message': 'Image received successfully'})

if __name__ == '__main__':
    app.run(debug=True)
