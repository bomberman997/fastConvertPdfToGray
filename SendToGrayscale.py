#Author: Bomberman997
#Date:6/6/2021
#Dropping a shortcut to this in your AppData\SentTo folder will allow you to 
#right click on any pdf and convert to grayscale copy on the spot

##REQUIRES POPPLER TO WORK. LINK IN README

from pdf2image import convert_from_path
from tempfile import TemporaryDirectory
import os,cv2
from glob import glob
from img2pdf import convert
import sys

#uses pdf2image to convert each page of PDF to PNG
def make_img(filename_,tmp_dir):
    path = r"{0}".format(filename_)
    imge_obj = convert_from_path(
        filename_,
        output_folder=tmp_dir,
        fmt="png",
        thread_count=4,
        poppler_path=r'C:\Program Files\poppler-0.68.0_x86\poppler-0.68.0\bin'
    )
    return imge_obj

#pdf2image has a grayscale option but cv2 is a fanstatic lib for grayscale
def to_grayscale(imagelist):
    for xx in imagelist:
        img = cv2.imread(xx,cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(xx,img)

def main(filename):
    with TemporaryDirectory() as temp_dir:

        images = make_img(filename,temp_dir)
        image_list = list()

        #adds each image filename and path to list plus each image object to another list(image_list,images)
        for page_number in range(1, len(images) + 1):
            path = os.path.join(temp_dir, "page_" + str(page_number) + ".PNG")
            image_list.append(path)
            images[page_number-1].save(path, "PNG") # (page_number - 1) because index starts from 0

        to_grayscale(image_list)

        #Outputs list of files and PNGS as final pdf, overwrites original
        with open(filename, "bw") as gray_pdf:
            gray_pdf.write(convert(image_list))

if __name__ == '__main__':
    main(sys.argv[1])