import os
import struct

def get_png_width(path):
    with open(path, 'rb') as f:
        data = f.read(24)
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            width, height = struct.unpack('>LL', data[16:24])
            return width
    return None

path = r'd:\Nong Trai\assets\Crops'
for file in os.listdir(path):
    if file.endswith('.png'):
        full_path = os.path.join(path, file)
        width = get_png_width(full_path)
        if width:
            print(f"{file}: Width={width}, Frames={width//16}")
