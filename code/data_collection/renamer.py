import os

path = '/home/marcus1/Documents/data_collection/drift_data_25092024'

files = os.listdir(path)
print(files)

input('ok? ')
for file in files:
    new_name = file[:6] + '.jpg'
    print(new_name)
    os.rename(os.path.join(path, file), os.path.join(path,new_name))