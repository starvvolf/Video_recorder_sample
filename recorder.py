# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 23:37:47 2024

@author: jkh01
"""

import cv2 as cv
import numpy as np
import time
from datetime import datetime


sample='rtsp://210.99.70.120:1935/live/cctv001.stream'
ID = 0
video = cv.VideoCapture(ID)
video.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

brightness=0
contrast=50

def update_brightness(val):
    global brightness
    brightness = val

def update_contrast(val):
    global contrast
    contrast = val


prev_time=0
fps_set=10

if video.isOpened():

    
    fps = video.get(cv.CAP_PROP_FPS)
    record = False
    now = datetime.now().strftime("%d_%H-%M-%S")

    fourcc = cv.VideoWriter_fourcc('X','V','I','D')  # 설정에 맞게 수정하세요.

    while True:
        # 비디오에서 프레임을 읽어옵니다.
        ret, frame = video.read()
        

        # 프레임을 읽어오지 못했거나, 비디오의 마지막까지 도달했으면 루프를 종료합니다.
        if not ret:
            break

        # 현재 비디오 프레임의 인덱스를 가져옵니다.
        current_frame_index = int(video.get(cv.CAP_PROP_POS_FRAMES))

        if record:  # 녹화 중일 때만 프레임을 녹화합니다.
            cv.circle(frame, (10, 10), radius=5, color=(0, 0, 255), thickness=-1)


        frame = cv.convertScaleAbs(frame, alpha=contrast/50.0, beta=brightness)
        cv.putText(frame, f"Brightness: {brightness}", (10, frame.shape[0] - 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv.putText(frame, f"Contrast: {contrast}", (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv.putText(frame, f"FPS: {int(fps)}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        # 비디오 프레임을 화면에 표시합니다.
        cv.imshow('Video', frame)

        # 사용자의 입력을 대기합니다.
        key = cv.waitKey(1)

        if key == 27:  # ESC
            break

        if key == ord(' '):  # 스페이스바를 누르면 녹화/비녹화 모드를 전환합니다.
            record = not record
            if record:
                print("record")
                video_writer = cv.VideoWriter(str(now) + ".avi", fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            else:
                print("recorded")
                if video_writer is not None:
                    video_writer.release()
                    video_writer = None

        if record and video_writer is not None:  # 녹화 중일 때만 프레임을 녹화합니다.
            video_writer.write(frame)
            
        if key == ord('p'):
            brightness = min(brightness + 1, 100)
       
        elif key == ord('o'):
            brightness = max(brightness - 1, -100)
      
        elif key == ord('k'):
            contrast = min(contrast + 1, 100)
       
        elif key == ord('j'):
            contrast = max(contrast - 1, 0)

    

# 비디오 재생이 끝나면 모든 창을 닫습니다.
cv.destroyAllWindows()
