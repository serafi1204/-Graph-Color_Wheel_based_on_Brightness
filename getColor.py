import cv2
import numpy as np
import math

def HSV2BRG(H, S, V):
    cv = np.ones((1, 1, 3))
    cv[0, 0, :] = (H, S, V)
    cv = cv.astype(np.uint8)
    cvBRG = cv2.cvtColor(cv, cv2.COLOR_HSV2BGR)
    
    return cvBRG[0, 0, :]

def HSV2GRAY__(H):
    cv = np.ones((1, 1, 3))
    cv[0, 0, :] = (H, 255, 255)
    cvRGB = cv2.cvtColor(cv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    B, G, R = cvRGB[0, 0, :]
    
    return 0.257*R+0.504*G+0.089*B 
    
def HSV2GRAY(H):
    return (HSV2GRAY__(math.ceil(H)) * (H-math.floor(H)) + HSV2GRAY__(math.floor(H)) * (math.ceil(H)-H))

def rescaling(s):
    para = [0, 120, 180, 210, 240, 330, 360]
    sdot = 0
    
    for i in range(1,7):
        if (s<=para[i]):
            sdot = 60 * ((i-1) + (s-para[i-1])/(para[i]-para[i-1]))
            break
        
    return int(sdot)
