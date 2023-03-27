import zipfile36 as zipfile
import os

path = '/home/petru/Downloads/Down (copy)/'

def encrypted(zip_file):
    zf = zipfile.ZipFile(zip_file)
    for zinfo in zf.infolist():
        is_encrypted = zinfo.flag_bits & 0x1 
        if is_encrypted:
            return True
        else:
            return False
           
for filename in os.listdir(path):
    curr_file = path + filename
    if zipfile.is_zipfile(curr_file):
        if not encrypted(curr_file):
            zip = zipfile.ZipFile(curr_file)
            new_folder = curr_file[:len(curr_file)-4]

            if os.path.exists(new_folder):
                os.removedirs(new_folder)

            os.makedirs(new_folder)
            zip.extractall(new_folder)
            os.remove(curr_file)