import os,cv2
from ctypes import c_char_p
from PIL import Image
import numpy as np
for f in os.listdir('adult'):
    with open(f'adult/{f}','rb') as ff:
        bs=ff.read()
    offset=0x2c
    if bs[offset:offset+6]==b'TLG6.0':
        pass
    else:
        df=(c_char_p(bs[offset:offset+100]).value.decode('utf8'))
        offset+=len(df)+1 
        baseimg=cv2.imread(rf'extract/{df[1:]}.hzc.png')
        dimg=cv2.imread(rf'extract/{f}.png') 
         
        #cv2.imwrite(rf'merge/{f}.png',dimg+baseimg)  
        mask = cv2.inRange(dimg, (255, 255, 255), (255, 255, 255))
        dimg[mask == 255] = [0, 0, 0]
        baseimg[mask!=255]=[0,0,0]
        cv2.imwrite(rf'merge/{f}.png',baseimg+dimg) 