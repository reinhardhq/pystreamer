#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import traceback
import logging
import uuid
import asyncio
import time

import cv2
from retry import retry


# コマンドライン実行引数処理
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true')
parser.add_argument('--cameras', nargs='*')
args = parser.parse_args()

# RTSP Server
SERVER = "rtsp://localhost:8554/live.sdp"

# スライス後静止画の保存先ディレクトリ
save_dir = os.path.dirname(os.path.abspath(__file__)) + '/pictures/'

#######################################
#
# Logger
#
#######################################
logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.INFO, filename='app.log', format=fmt)


@retry()
async def capture_stream(server):
    i = 0
    logger.info('request server address is {0}'.format(server))

    loop = asyncio.get_event_loop()

    cap = cv2.VideoCapture(server)

    is_exist = cap.isOpened()

    # streamがOpenできない場合はreturnする
    if not is_exist:
        logger.warning('{0} can not open stream'.format(server))
        return
    # streamがOpenできる場合は処理を継続する
    else:
        # await loop.run_in_executor(None)

        logger.info('{0} capture stream start'.format(server))

        await loop.run_in_executor(__capture(i, cap))
        # stream_id = None
        #
        # while (cap.isOpened()):
        #     ret, frame = cap.read()
        #
        #     # debug指定時はGUIに映像ストリームを表示する
        #     if args.debug:
        #         cv2.imshow('Raw Frame', frame)
        #
        #         # 映像ストリームの取得が始まった場合、 `q` を入力すると break する
        #         if cv2.waitKey(20) & 0xFF == ord('q'):
        #             break
        #     # 通常はimwriteによりスライスした静止画を保存する
        #     else:
        #
        #         if stream_id is None:
        #             stream_id = str(uuid.uuid4())
        #         file_name = stream_id + '_' + str(i) + '.png'
        #         file_name = save_dir + file_name
        #
        #         time.sleep(1)
        #         cv2.imwrite(file_name, frame)
        #         i += 1
        #
        # cap.release()
        # cv2.destroyAllWindows()


def __capture(i, cap):
    stream_id = None

    while (cap.isOpened()):
        ret, frame = cap.read()

        # debug指定時はGUIに映像ストリームを表示する
        if args.debug:
            cv2.imshow('Raw Frame', frame)

            # 映像ストリームの取得が始まった場合、 `q` を入力すると break する
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        # 通常はimwriteによりスライスした静止画を保存する
        else:

            if stream_id is None:
                stream_id = str(uuid.uuid4())
            file_name = stream_id + '_' + str(i) + '.png'
            file_name = save_dir + file_name

            time.sleep(1)
            cv2.imwrite(file_name, frame)
            i += 1

    cap.release()
    cv2.destroyAllWindows()


def multi_capture_streams(camera_list):
    loop = asyncio.get_event_loop()
    print(camera_list[0])
    print(camera_list[1])

    gather = asyncio.gather(
        capture_stream(camera_list[0]),
        capture_stream(camera_list[1])
    )
    loop.run_until_complete(gather)


if __name__ == '__main__':
    try:
        if len(args.cameras) != 0:
            multi_capture_streams(args.cameras)
        else:
            capture_stream(SERVER)
    except:
        logger.error(traceback.format_exc())