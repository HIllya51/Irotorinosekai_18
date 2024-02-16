import os
from ctypes import c_uint,c_char_p
with open('graph.bin','rb') as ff:
    bs=bytearray(ff.read())
with open('graph.bin','rb') as ff:
    newbs=bytearray(ff.read())
count=c_uint.from_buffer_copy(bs[:4]).value
print(count)
index_size=count*12
name_index_size=c_uint.from_buffer_copy(bs[4:8]).value
print(name_index_size)
index_offset=8
names_base=index_offset + index_size
print(hex(names_base))
newoff=0
for i in range(count):
    filename_offset=c_uint.from_buffer_copy(bs[index_offset:index_offset+4]).value
    
    #print(hex(filename_offset))
    name=c_char_p(bytes(bs[names_base+filename_offset:names_base+filename_offset+ 100])).value.decode('shiftjis')
    #print(name)
    offset=c_uint.from_buffer_copy(bs[index_offset+4:index_offset+8]).value
    size=c_uint.from_buffer_copy(bs[index_offset+8:index_offset+12]).value
    #print(hex(offset),hex(size))
    if i==0:
        newbs=newbs[:offset]
        newoff=offset
    newbs[index_offset+4:index_offset+8]=bytes(c_uint(newoff))
    try:
        with open(f'hzc/{name}','rb') as ff:
            bb=bytearray(ff.read())
        print(len(bb),size)
        newoff+=len(bb)
        newbs[index_offset+8:index_offset+12]=bytes(c_uint(len(bb)))
        newbs+=bb
    except:
        newbs+=bs[offset:offset+size] 
        newoff+=size
    
    index_offset+=12
with open('graph.bin','wb') as ff:
    ff.write(newbs)