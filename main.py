from fer import FER
import cv2
import matplotlib.pyplot as plt
from moviepy.editor import *
import os

audioclip = AudioFileClip('D:/01-01-01-01-01-01-01.mp4')  # видеофайл 1.mp4
audioclip.write_audiofile('D:/out_audio.mp3')  # извлеченная аудиодорожка в файл out_audio.mp3

test_img = cv2.imread('D:/Kirill.jpg')
plt.imshow(test_img[:, :, ::-1])
emo_detector = FER(mtcnn=True)
captured_emotions = emo_detector.detect_emotions(test_img)
print(captured_emotions)
dominant_emmotion, emotion_score = emo_detector.top_emotion(test_img)
print(dominant_emmotion, emotion_score)


cam = cv2.VideoCapture("D:/Actor_01/01-01-04-02-01-01-01.mp4")

try:
    if not os.path.exists('data'):
        os.makedirs('data')

except OSError:
    print('Error: Creating directory of data')

intvl = 1 #interval in second(s)

fps= int(cam.get(cv2.CAP_PROP_FPS))
print("fps : " ,fps)

currentframe = 0
while (True):
    ret, frame = cam.read()
    if ret:
        if(currentframe % (fps*intvl) == 0):
            name = './data/frame' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)
            test_img = cv2.imread(name)
            plt.imshow(test_img[:, :, ::-1])
            emo_detector = FER(mtcnn=True)
            captured_emotions = emo_detector.detect_emotions(test_img)
            print(captured_emotions)
            dominant_emmotion, emotion_score = emo_detector.top_emotion(test_img)
            print(dominant_emmotion, emotion_score)

        currentframe += 1

    else:
        break

cam.release()
cv2.destroyAllWindows()
