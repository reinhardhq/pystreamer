#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import traceback
import logging
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


@retry(delay=5, backoff=2, max_delay=60)
@asyncio.coroutine
def capture_stream_1(server):
    i = 0
    logger.info('T1')
    logger.info('request server address is {0}'.format(server))

    # loop = asyncio.get_event_loop()

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
        # __capture(i, cap, 't1')
        while (cap.isOpened()):
            ret, frame = cap.read()

            yield from asyncio.sleep(1)

            logger.info('t1 {0} streaming...'.format(server))

            # debug指定時はGUIに映像ストリームを表示する
            if args.debug:
                cv2.imshow('Raw Frame', frame)

                # 映像ストリームの取得が始まった場合、 `q` を入力すると break する
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            # 通常はimwriteによりスライスした静止画を保存する
            else:
                file_name = 't1' + '_' + str(i) + '.png'
                file_name = save_dir + file_name

                time.sleep(1)
                cv2.imwrite(file_name, frame)
                i += 1

        cap.release()
        cv2.destroyAllWindows()


@retry(delay=5, backoff=2, max_delay=60)
@asyncio.coroutine
def capture_stream_2(server):
    i = 0
    logger.info('T2')
    logger.info('request server address is {0}'.format(server))

    # loop = asyncio.get_event_loop()

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

        # __capture(i, cap, 't2')

        while (cap.isOpened()):

            yield from asyncio.sleep(1)

            ret, frame = cap.read()

            logger.info('t2 {0} streaming...'.format(server))

            # debug指定時はGUIに映像ストリームを表示する
            if args.debug:
                cv2.imshow('Raw Frame', frame)

                # 映像ストリームの取得が始まった場合、 `q` を入力すると break する
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            # 通常はimwriteによりスライスした静止画を保存する
            else:
                file_name = 't2' + '_' + str(i) + '.png'
                file_name = save_dir + file_name

                time.sleep(1)
                cv2.imwrite(file_name, frame)
                i += 1

        cap.release()
        cv2.destroyAllWindows()


# def __capture(i, cap, t):
#
#     while (cap.isOpened()):
#         ret, frame = cap.read()
#
#         # debug指定時はGUIに映像ストリームを表示する
#         if args.debug:
#             cv2.imshow('Raw Frame', frame)
#
#             # 映像ストリームの取得が始まった場合、 `q` を入力すると break する
#             if cv2.waitKey(20) & 0xFF == ord('q'):
#                 break
#         # 通常はimwriteによりスライスした静止画を保存する
#         else:
#             file_name = t + '_' + str(i) + '.png'
#             file_name = save_dir + file_name
#
#             time.sleep(1)
#             cv2.imwrite(file_name, frame)
#             i += 1
#
#     cap.release()
#     cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        if len(args.cameras) != 0:
            loop = asyncio.get_event_loop()
            tasks = asyncio.wait([capture_stream_1(args.cameras[0]), capture_stream_2(args.cameras[1])])
            loop.run_until_complete(tasks)

        else:
            capture_stream_1(SERVER)
    except:
        logger.error(traceback.format_exc())