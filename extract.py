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
        with open('tmp','wb') as ff:
            ff.write(bs[0x2c:])
        os.system(rf'Project1\x64\Release\Project1.exe tmp')
        try:
            os.remove(rf'extract/{f}.png')
        except:pass
        os.rename('tmp.png',rf'extract/{f}.png')
    else:
        df=(c_char_p(bs[offset:offset+100]).value.decode('utf8'))
        offset+=len(df)+1
        print(bs[offset:offset+6])
        with open('tmp','wb') as ff:
            ff.write(bs[offset:])
        os.system(rf'Project1\x64\Release\Project1.exe tmp')
        try:
            os.remove(rf'extract/{f}.png')
        except:pass
        os.rename('tmp.png',rf'extract/{f}.png')
        # baseimg=cv2.imread(rf'extract/{df[1:]}.hzc.png')
        # dimg=cv2.imread(rf'extract/{f}.d.png') 
        
        # baseimg[dimg[:,:]!=(255,255,255)]=0
        # dimg[dimg[:,:]==(255,255,255)]=0
        # cv2.imwrite(rf'extract/{f}.png',dimg+baseimg) 