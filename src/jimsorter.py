import exifread
import os
import shutil
import errno

inpath = "/home/maibes/Desktop/Pictures"
outpath = "/home/maibes/Desktop/Pictures_Sorted"

def list_files(dir):
    r = []
    subdirs = [x[0] for x in os.walk(dir)]

    print(subdirs)
    for subdir in subdirs:
        result = next(os.walk(subdir))
        r.append(result)
    return r

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

for tuple in list_files(inpath):
    os.chdir(tuple[0])

    for filename in tuple[2]:
        filepath = tuple[0] + "/" + filename
        f = open(filepath, 'rb')

        tags = exifread.process_file(f, details=False)

        # for tag in tags.keys():
        #     if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        #         print("Key: %s, value %s" % (tag, tags[tag]))

        # for tag in tags.keys():
        #     if tag in ('EXIF DateTimeDigitized', 'Image DateTime'):
        #         print("Key: %s, value: %s" % (tag, tags[tag]))



        datetimetag = str(tags.get('Image DateTime', "Undated"))
        # datetimetag = str(exifread.process_file(f, details=False).get('EXIF DateTimeDigitized', "Undated")) 
        # print(datetimetag)

        if not datetimetag.startswith("2"):
            datetimetag = "Undated"

        destfolder = datetimetag[:7].replace(":", "-")
        print(destfolder)
        make_sure_path_exists(outpath + "/" + destfolder)
        if filename.startswith('email'):
            destpath = outpath + "/" + destfolder + "/" + filename.replace("email", "photo")
        else:
            destpath = outpath + "/" + destfolder + "/" + filename

        if not os.path.exists(destpath) and not filename.startswith("Thumb"):
            shutil.copy2(filepath, destpath)
        else:
            if not filename.startswith('IMG_'):
                duplicateindex = 2
                while os.path.exists(destpath + "_" + str(duplicateindex)):
                    duplicateindex += 1
                destpath = destpath + "_" + str(duplicateindex)
                shutil.copy2(filepath, destpath)
