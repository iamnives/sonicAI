import numpy as np 
import mss
import cv2
import time
from directkeys import W, A, S, D, PressKey, ReleaseKey


def draw_lines(image, lines):
    try:
        for line in lines:
            coord = line[0]
            cv2.line(image, (coord[0], coord[1]), (coord[2], coord[3]), [255,255,255], 3)
    except:
        pass

def p_region(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(image, mask)
    return masked


def process(og_image):
    vertices = np.array([ [10, 500 ], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500] ])
    pc_image = p_region(og_image, [vertices])
    pc_image = cv2.Canny(pc_image, threshold1=300, threshold2=400)
    pc_image = cv2.GaussianBlur(pc_image, (5,5), 0)
    #ratio is now 800x450 this is broken fix later
   
    #pc_image canny edges                            minlengt maxgap
    lines = cv2.HoughLinesP(pc_image, 1, np.pi/180, 180, np.array([]), 100, 5)
    draw_lines(pc_image, lines)

    return pc_image

def main():
    last_time = time.time()
    with mss.mss() as sct:
        monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 450}

        while(True):
            img = np.array(sct.grab(monitor))
            new_image = process(img)

            
            cv2.imshow('sonicAI', new_image)

            print('Loop time {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

main()