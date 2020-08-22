import cv2
import os

from os.path import splitext, basename


def extractImages(
    pathIn: str,
    pathOut='output',
    sec=1,
    ext='jpg'
):

    # CAP_PROP_POS_MSEC	0       再生位置を時間で表したもの（ミリ秒単位）
    # CAP_PROP_POS_FRAMES	1   再生中のフレーム番号
    # CAP_PROP_FRAME_WIDTH	3	フレームの幅
    # CAP_PROP_FRAME_HEIGHT	4	フレームの高さ
    # CAP_PROP_FPS	5           フレームレート
    # CAP_PROP_FRAME_COUNT	7	全フレーム数

    # ファイル名のパスを生成
    v_name = splitext(basename(pathIn))[0]
    base_path = os.path.join(pathOut, v_name)

    # pathOutが存在しない場合はディレクトリを作る.
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    cap = cv2.VideoCapture(pathIn)

    if not cap.isOpened():
        return

    # 総フレーム数とfpsを取得
    all_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_inv = 1 / fps

    # 動画の総時間
    all_time = all_frame / fps

    print('all time', all_time)
    print('get frames', all_time / sec)

    # 桁を取得
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    # 秒感覚 fps x sec(秒)
    sec_range = fps * sec
    # print(round(fps/4))

    for idx in range(0, int(all_frame), round(sec_range)):
        print(idx, all_frame)

        # フレームの位置を設定
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)

        # 現在の再生位置（フレーム位置）の取得
        current_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_pos = str(current_pos)

        ret, frame = cap.read()

        if ret:
            filename = '{}_{}.{}'.format(
                str(idx).zfill(digit), round(idx * fps_inv), ext
            )
            save_path = os.path.join(base_path, filename)
            cv2.imwrite(save_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

            # print(save_path)
            # print('--' * 30)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    extractImages(pathIn='shibuya_night.mp4', pathOut='output', sec=3)


# if __name__ == "__main__":
#     main()
