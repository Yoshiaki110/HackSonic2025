from flask import Flask, request, jsonify, render_template, send_from_directory
import base64
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
def upload_image():
    data = request.json
    image_data = data['image']
    file_name = data['fileName']
    finish = data['finish']
    image_data = image_data.split(",")[1]  # data URLのヘッダを削除
    image_bytes = base64.b64decode(image_data)

    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    with open(file_path, 'wb') as f:
        f.write(image_bytes)

    print('finish', finish)
    return jsonify({'message': '画像が保存されました'}), 200

if __name__ == '__main__':
    app.run(debug=True)
