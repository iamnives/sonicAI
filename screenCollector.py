import numpy as np 
import mss
import cv2
import time


last_time = time.time()


with mss.mss() as sct:
    monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 640}

    while(True):
        img = np.array(sct.grab(monitor))
        cv2.imshow('sonicAI', img)

        print('Loop time {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break