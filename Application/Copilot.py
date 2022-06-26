#!/usr/bin/env python3

# this is script is used to create zip folder and files

# this function zip the folder and files
def zip_folder(folder_path, zip_file_path):
    import zipfile
    import os

    # create zip file
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

    # walk through the folder
    for root, dirs, files in os.walk(folder_path):
        # add the files to the zip
        for file in files:
            zip_file.write(os.path.join(root, file))
    # close the zip
    zip_file.close()
    return zip_file_path

zip_folder('tests', 'test.zip')
