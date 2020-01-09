# pystreamer

* 以下のSERVERで接続先を指定しています。適宜変更して下さい。

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
SERVER = "localhost:8554/live.sdp"

(省略)

```
