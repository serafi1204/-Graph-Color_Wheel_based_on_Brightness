import cv2
import numpy as np
import colorsys
import math

from getPolarAxis import *
from getColor import *

# dp
dp = {}

# Canvas
size = 500
radius = round(size/2)
offset = 10
cvSize = size + offset*2

# function
def getSeta(x, y, r):
    s = np.arccos(x/r)*180/np.pi if r != 0 else 0
    if (y > 0):
        s = 360-s
    s = rescaling(s)
    s = (s+120)%360
    
    return s

# draw H-V wheel
cvHV = np.ones((cvSize, cvSize, 4)) * 150
cvHV[:, :, 3] = 0
cvHS = np.ones((cvSize, cvSize, 4)) * 150
cvHS[:, :, 3] = 0
cvHSV = np.ones((cvSize, cvSize, 4)) * 150
cvHSV[:, :, 3] = 0

for x in range(-radius, radius+1):
   for y in range(-radius, radius+1): 
        r = np.sqrt(x**2+y**2)
        s = getSeta(x, y, r)
        
        rate = dp[s] if dp.get(s) else (HSV2GRAY((s+240)%360/359*179)/255)
        rate = rate if rate != 0 else 0.26

        xx = round(x + offset + radius)
        yy = round(y + offset + radius)
        
        if (r >= rate*radius and r <= radius):
            c = HSV2BRG(
                round((s+240)%360/360*179),
                round((radius-r)/radius/(1-rate)*255) if rate != 0 else 0,
                255
            )
            
            cvHS[yy, xx, 0:3] = c
            cvHS[yy, xx, 3] = 255
            cvHSV[yy, xx, 0:3] = c
            cvHSV[yy, xx, 3] = 255
            
        elif (r <= rate*radius):
            c = HSV2BRG(
                round((s+240)%360/360*179),
                255,
                round(r/radius/rate*255) if rate != 0 else 0
            )
            
            cvHV[yy, xx, 0:3] = c
            cvHV[yy, xx, 3] = 255
            cvHSV[yy, xx, 0:3] = c
            cvHSV[yy, xx, 3] = 255
            
cv2.imwrite(f'H-V.jpg',cvHV)  
cv2.imwrite(f'H-S.jpg',cvHS) 
cv2.imwrite(f'H-SV.jpg',cvHSV) 

# add grid

def addGray(cv, x, y):
    if (cv[x, y, 3] == 255):
        cv[x, y, :] -= - 150
    else:
        cv[x, y, :] = 255
        
    return cv
    
    
for x in range(-radius, radius+1):
    for y in range(-radius, radius+1): 
        r = np.sqrt(x**2+y**2)
        s = np.arccos(x/r)*180/np.pi if r != 0 else 0
        if (y > 0):
            s = 360-s
        s = (s+30)%360
        
        if (r <= radius+1):
            if (int(r%(radius/5)) == 0 or round(s)%30 == 0):
                xx = round(x + offset + radius)
                yy = round(y + offset + radius)
                
                cvHV[xx, yy, 3] = 200
                cvHS[xx, yy, 3] = 200
                cvHSV[xx, yy, 3] = 200

for x in range(5):     
    r = 1/5*(x+1)
    cvHV = cv2.putText(cvHV, f"{int(r*100)}%", (int(offset+radius*(1+r)+2), offset+radius-2),
        cv2.FONT_HERSHEY_DUPLEX, 0.15/200*size, (0, 0, 0), 1, cv2.LINE_AA)
    cvHS = cv2.putText(cvHS, f"{int(r*100)}%", (int(offset+radius*(1+r)+2), offset+radius-2),
        cv2.FONT_HERSHEY_DUPLEX, 0.15/200*size, (0, 0, 0), 1, cv2.LINE_AA)
    cvHSV = cv2.putText(cvHSV, f"{int(r*100)}%", (int(offset+radius*(1+r)+2), offset+radius-2),
        cv2.FONT_HERSHEY_DUPLEX, 0.15/200*size, (0, 0, 0), 1, cv2.LINE_AA)
                

                
cv2.imwrite(f'H-V_grid.jpg',cvHV)  
cv2.imwrite(f'H-S_grid.jpg',cvHS) 
cv2.imwrite(f'H-SV_grid.jpg',cvHSV) 
