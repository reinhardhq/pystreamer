#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import cv2

# コマンドライン実行引数処理
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true')
args = parser.parse_args()

# RTSP Server
SERVER = "localhost:8554/live.sdp"

# スライス後静止画の保存先ディレクトリ
save_dir = os.path.dirname(os.path.abspath(__file__)) + '/pictures/'

if __name__ == '__main__':
    i = 0
    cap = cv2.VideoCapture('rtsp://'+SERVER)

    while(cap.isOpened()):
        ret, frame = cap.read()

        # debug指定時はGUIに映像ストリームを表示する
        if args.debug:
            cv2.imshow('Raw Frame', frame)

            # 映像ストリームの取得が始まった場合、 `q` を入力すると break する
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        # 通常はimwriteによりスライスした静止画を保存する
        else:
            file_name = 'stream_' + str(i) + '.png'
            file_name = save_dir + file_name

            cv2.imwrite(file_name, frame)
            i += 1

    cap.release()
    cv2.destroyAllWindows()