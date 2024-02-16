import os,shutil
# for f in os.listdir('extract'):
#     os.system(rf'python nvsg_converter.py --encode extract/{f} hzc/{f[:-4]}')

# for f in os.listdir('hzc'):
#     os.rename('hzc/'+f,'hzc/'+f[:-4])

# for f in os.listdir('hzc'):
#     ok=False
#     for vis in ['graph_vis','graph_vis1','graph_vis2']:
#         if os.path.exists(f'{vis}/{f}'):
#             shutil.copy(f'hzc/{f}',f'{vis}/{f}')
#             ok=True
    # if ok==False:
    #     print(f)
# for vis in ['graph_vis','graph_vis1','graph_vis2']:
#     os.system(f'python bin_archiver.py -c {vis} {vis}.bin')