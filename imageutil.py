from PIL import Image
import printutil

stop = False

def conv(dir, id, ovl, printer):
    face_image = Image.open(dir + id + '.png')
    sign_image = Image.open(dir + ovl)

    # サインの画像を左に90度回転させる
    sign_image = sign_image.rotate(90, expand=True)

    # サインの画像を顔の画像と同じ大きさにリサイズ
    sign_image = sign_image.resize(face_image.size)

    # サインの画像を2値化する（黒か白にする）
    sign_image = sign_image.convert("L")
    sign_image = sign_image.point(lambda x: 0 if x < 128 else 255, '1')

    # サインの画像を透過画像にする（黒の部分を赤にする）
    sign_image = sign_image.convert("RGBA")
    data = sign_image.getdata()

    new_data_w = []
    new_data_b = []
    for item in data:
        # 黒を赤に、白は透明に
        if item[0] == 0:
            new_data_w.append((256, 17, 195, 255))  # ピンクに設定
            new_data_b.append((0, 0, 0, 255))        # 黒に設定
        else:
            new_data_w.append((255, 255, 255, 0))  # 透明に設定
            new_data_b.append((0, 0, 0, 0))        # 透明に設定

    sign_image.putdata(new_data_b)
    # 顔の画像に透過サインの画像をオーバーレイする
    face_image.paste(sign_image, (3, 3), sign_image)

    sign_image.putdata(new_data_w)
    # 顔の画像に透過サインの画像をオーバーレイする
    face_image.paste(sign_image, (0, 0), sign_image)

    # 画像をRGBモードに変換してからJPGとして保存する
    face_image = face_image.convert("RGB")
    face_image.save(dir + id + '.jpg', 'JPEG')
    # 印刷
    if not stop:
        printutil.print(dir + id + '.jpg', printer)

if __name__ == '__main__':
    stop = True
    dir = 'uploads/'
    #conv(dir, 'e3bf3ea4-415b-48c9-a52e-36604e5800be', 'scan.jpg')
    conv(dir, 'fb531baf-a0b6-41a8-a59a-afc7905ea942', 'scan.jpg')

