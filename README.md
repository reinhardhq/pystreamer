# pystreamer


* 実行

複数ストリーム取得
```python

$ python pystreamer.py --cameras rtsp://localhost:8554/live.sdp rtsp://localhost:8555/live.sdp

```

単一ストリーム取得
```python

$ python pystreamer.py --cameras rtsp://localhost:8554/live.sdp

 or

$ python pystreamer.py

```


* 単一ストリーム取得かつ--camerasオプションを利用しない場合、以下のSERVERで指定した接続先を利用しています。適宜変更して下さい。

```python

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
SERVER = "rtsp://localhost:8554/live.sdp"

(省略)

```


* リトライ
    * リトライとして一般的なExponential Backoff(指数関数的後退)を利用しています。
    * （リトライ間隔が「倍、倍・・」になるアルゴリズム）
    * 最大遅延を60secとし、初回の再実行時間遅延を5secにしています。

```python
@retry(delay=5, backoff=2, max_delay=60)
```