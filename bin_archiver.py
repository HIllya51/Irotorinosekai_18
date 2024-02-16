#!/usr/bin/python3
import os
import re
import sys
from open_ext import open_ext

def get_table_size(file_count):
    return file_count * 12

def name_to_path(i, name):
    #return '%04d_%s' % (i, name.decode('sjis'))
    return '%s' % (name.decode('sjis'))
def path_to_name(path):
    return re.sub('^\d+_', '', os.path.basename(path)).encode('sjis')

def extract(file_path, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with open_ext(file_path, 'rb') as file:
        file_count = file.read_u32_le()
        file_names_size = file.read_u32_le()
        file_names_start = file.tell() + get_table_size(file_count)
        for i in range(file_count):
            file_name_offset = file.read_u32_le()
            offset = file.read_u32_le();
            size = file.read_u32_le();

            old_pos = file.tell()
            file.seek(file_names_start + file_name_offset)
            name = name_to_path(i, file.read_until_zero())
            file.seek(offset)
            content = file.read(size)
            file.seek(old_pos)

            target_path = os.path.join(target_folder, name)
            print('Saving to %s...' % target_path)
            with open(target_path, 'wb') as target_file:
                target_file.write(content)

def pack(source_folder, file_path):
    source_paths = [os.path.join(source_folder, f) for f in os.listdir(source_folder)]
    source_paths.sort()
    names = [path_to_name(path) for path in source_paths]
    with open_ext(file_path, 'w+b') as file:
        file.write_u32_le(len(names))
        file.write_u32_le(sum([len(name) + 1 for name in names]))
        file.write(b"\x00" * get_table_size(len(names)))

        table = [{} for i in names]

        file_names_start = file.tell()
        print(file_names_start)
        for i, name in enumerate(names):
            table[i]['name_offset'] = file.tell() - file_names_start
            file.write(name)
            file.write(b"\x00")

        for i, source_path in enumerate(source_paths):
            print('Writing %s...' % (source_paths[i]))
            table[i]['file_offset'] = file.tell()
            with open(source_path, 'rb') as source_file:
                file.write(source_file.read())
            table[i]['file_size'] = file.tell() - table[i]['file_offset']

        file.seek(8)
        for i, entry in enumerate(table):
            file.write_u32_le(entry['name_offset'])
            file.write_u32_le(entry['file_offset'])
            file.write_u32_le(entry['file_size'])

def main():
    if len(sys.argv) == 4:
        if sys.argv[1] == '-d':
            extract(sys.argv[2], sys.argv[3])
            return
        elif sys.argv[1] == '-c':
            pack(sys.argv[2], sys.argv[3])
            return

    print('Usage: script.py -d input.bin folder')
    print('Usage: script.py -c folder output.bin')
    print('-d: extracts files from the input.bin archive file into given folder')
    print('-c: packs given folder back into an output.bin to use in game')
    print('')
    print('NOTE: when packing, make sure the folder doesn\'t contain any files other')
    print('than files unpacked from original archive, otherwise the game will crash.')
    print('This is a limitation of FVP games since they expect a fixed number of files.')

if __name__ == '__main__':
    main()
