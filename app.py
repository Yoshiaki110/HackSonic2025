from flask import Flask, request, jsonify, render_template, send_from_directory
import base64
from PIL import Image
from io import BytesIO
import os
import uuid
import imageutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

# プリンタからのサインの登録
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

# 印刷
@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data['image']
    printer = data['printer']

    # 画像データのBase64部分を取り出してデコード
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    # 画像を保存
    image = Image.open(BytesIO(image_bytes))
    id = str(uuid.uuid4())
    fname = UPLOAD_FOLDER + '/' + id + '.png'
    image.save(fname)
    imageutil.conv(UPLOAD_FOLDER + '/', id, 'scan.jpg', printer)

    return jsonify({'message': 'Image received successfully'})

if __name__ == '__main__':
    app.run(debug=True)
