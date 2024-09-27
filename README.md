# Slimeface
[![PyPI](https://img.shields.io/pypi/v/slimeface.svg)](https://pypi.python.org/pypi/slimeface)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)
## Introduction 
A super fast face detector packaged by the [libfacedetection](https://github.com/ShiqiYu/libfacedetection) repository using pybind11.
## Change Log
[2023-5-8] Project init.

[2024-9-27] Drop numpy dependency

## Quick start
```shell
pip install slimeface
```

### Usage
1. Load image
```python
# PIL
import PIL
import numpy as np
img = PIL.Image.open('xxx.jpg').convert('RGB')
```

2. Detect
```python
# img: numpy.ndarray, shape=(H, W, 3), dtype=uint8, BGR
# conf_thresh: float, confidence threshold, default=0.5, range=[0.0, 0.1]
from slimeface import detectRGB
bbox_confs = detectRGB(img.width, img.height, img.tobytes())
```
3. Deal result
```python
# confs: numpy.ndarray, shape=(N,), dtype=uint16, confidence 
# bboxes: numpy.ndarray, shape=(N, 4), dtype=uint16, bounding box (XYWH)
# landmarks: numpy.ndarray, shape=(N, 10), dtype=uint16, landmarks (XYXYXYXYXY)
import cv2
for bbox_conf in bbox_confs:
    bbox = bbox_confs[:-1]
    conf = bbox_confs[-1]
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 1)
    cv2.putText(img, str(conf), (bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
cv2.imwrite('result.jpg', img)
```
![result](resources/result.jpg)
