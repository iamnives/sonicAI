import numpy as np
import cv2
import time
from numpy import ones,vstack
from numpy.linalg import lstsq
from directkeys import PressKey, W, A, S, D, ReleaseKey
from statistics import mean
from draw_lines import draw_lanes
import mss

def roi(img, vertices):
    
    #blank mask:
    mask = np.zeros_like(img)   
    
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, 255)
    
    #returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(image):
    original_image = image
    # edge detection
    processed_img =  cv2.Canny(image, threshold1 = 300, threshold2=400)
    
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    

    vertices = np.array([ [0, 450 ], [0, 175], [175, 100], [700, 100], [800, 175], [800, 450] , [600, 450], [500, 225], [300, 225 ], [200, 450] ], np.int32)

    processed_img = roi(processed_img, [vertices])

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho   theta   thresh  min length, max gap:        
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,  np.array([]),    250,       20)
    m1 = 0
    m2 = 0
    try:
        l1, l2, m2, m1 = draw_lanes(original_image,lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)

    except Exception as e:
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
                
                
            except Exception as e:
                pass
    except Exception as e:
        pass

    return processed_img,original_image, m1, m2

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    ReleaseKey(S)
    ReleaseKey(D)

def right():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    PressKey(D)

def breky():
    ReleaseKey(W)
    ReleaseKey(A)
    PressKey(S)
    ReleaseKey(D)

def drive(m1, m2):
    hor_threshold = 20

    if m1 < hor_threshold and m1 > hor_threshold*(-1) and m2 < hor_threshold and m2 > hor_threshold*(-1):
        straight()
        


    if m1 < 0 and m2 < 0:
        right()
    elif m1 > 0 and m2 > 0:
        left()
    else:
        straight()

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)


last_time = time.time()

monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 450}
with mss.mss() as sct:
    while True:
        screen = np.array(sct.grab(monitor))

        last_time = time.time()
        new_screen,original_image, m1, m2 = process_img(screen)
        cv2.imshow('sonicAI',original_image)
        cv2.imshow('window',new_screen)

        drive(m1, m2)
     
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

