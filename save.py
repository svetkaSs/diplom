from fer import FER
import cv2
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
import os
import xlwt
from array import *



def save_frame_range_sec(video_path, start_sec, stop_sec, step_sec, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    emot = list()
    emot_ver = list()
    cols = ['A', 'B']
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sad Sheet 1")
    index = 0

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_inv = 1 / fps

    sec = start_sec

    while sec < stop_sec:
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            name = './data/frame' + str(sec) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)
            test_img = cv2.imread(name)
            plt.imshow(test_img[:, :, ::-1])
            emo_detector = FER(mtcnn=True)
            captured_emotions = emo_detector.detect_emotions(test_img)
            print(captured_emotions)
            print(sec)
            dominant_emmotion, emotion_score = emo_detector.top_emotion(test_img)
            emot.append(dominant_emmotion)
            emot.append(emotion_score)

            print(dominant_emmotion, emotion_score)
            sec += step_sec

            cv2.imwrite(
                '{}_{}_{:.2f}.{}'.format(
                    base_path, str(n).zfill(digit), n * fps_inv, ext
                ),
                frame

            )


video_path = "D:/Actor_01/01-01-04-02-01-01-01.mp4"
clip = VideoFileClip(video_path)
save_frame_range_sec(video_path,
                     0, clip.duration, 1,
                     'D:/data', 'sample_video_img')


