import numpy as np 
import mss
import cv2
import time
import time
from directkeys import W, A, S, D, PressKey, ReleaseKey

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)


def process(og_image):
    pc_image = cv2.Canny(og_image, threshold1=200, threshold2=300)
    return pc_image


last_time = time.time()
with mss.mss() as sct:
    monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 600}

    while(True):
        PressKey(W)
        img = np.array(sct.grab(monitor))

        new_image = process(img)

        cv2.imshow('sonicAI', new_image)

        print('Loop time {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        ReleaseKey(W)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break