import cv2
import numpy as np
import printutil

# 縮小率
scale_percent = 50
stop = False

def debug(title, img):
    if not stop:
        return
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img_rotated = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    # 回転させた画像を表示
    cv2.imshow(title, resized_img_rotated)
    cv2.waitKey(0)

def conv(dir, id, ovl):
    # 'scan.jpg'を読み込み
    img = cv2.imread(dir + ovl)

    # 左に90度回転させる
    img_rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    debug('Rotated Image', img_rotated)

    # グレースケールに変換せずに２値化
    _, binary_img = cv2.threshold(img_rotated, 128, 255, cv2.THRESH_BINARY)
    debug('2chik', binary_img)

    # 'xxx-xxx.png'を読み込み
    overlay_img = cv2.imread(dir + id + '.png', cv2.IMREAD_UNCHANGED)
    debug('xxx-xxx.png', overlay_img)

    # PNG画像と同じサイズにリサイズ
    binary_img_resized = cv2.resize(binary_img, (overlay_img.shape[1], overlay_img.shape[0]))
    debug('resize', binary_img_resized)

    # マスクを1チャンネルに変換
    if len(binary_img_resized.shape) == 3:
        binary_img_resized = cv2.cvtColor(binary_img_resized, cv2.COLOR_BGR2GRAY)
    debug('binary_img_resized (1 channel)', binary_img_resized)

    # overlay_imgのアルファチャンネルを削除して3チャンネルにする
    if overlay_img.shape[2] == 4:
        overlay_img = overlay_img[:, :, :3]  # RGBAからRGBに変換
    debug('overlay_img without alpha', overlay_img)

    # 二値化した画像をマスクとして使用
    overlay_image = cv2.bitwise_and(overlay_img, overlay_img, mask=binary_img_resized)
    debug('overlay_image', overlay_image)

    # 'xxx-xxx.jpg'として保存
    cv2.imwrite(dir + id + '.jpg', overlay_image)

    # 印刷
    printutil.print(dir + id + '.jpg')
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    stop = True
    dir = 'uploads/'
    #conv(dir, 'e3bf3ea4-415b-48c9-a52e-36604e5800be', 'scan.jpg')
    conv(dir, 'fb531baf-a0b6-41a8-a59a-afc7905ea942', 'scan.jpg')
