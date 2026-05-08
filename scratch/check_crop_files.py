import os

path = r'd:\Nong Trai\assets\Crops'
for file in os.listdir(path):
    if file.endswith('.png'):
        full_path = os.path.join(path, file)
        size = os.path.getsize(full_path)
        print(f"{file}: {size}")
