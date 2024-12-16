# author: Longhao Zhang
# date: 2022-08-24
from fitz import fitz
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

def deletePDF(file_path):
    # 删除pdf第一页代码
    target_file_path = file_path[:-4] + '-copy' + '.pdf'
    # 读取文件
    pdfReader = PdfFileReader(open(file_path, 'rb'), strict=False)
    pdfFileWriter = PdfFileWriter()
    numPages = pdfReader.getNumPages()
    # 要删除的页面，注意起始页为0
    for index in range(1, numPages):
        pdfFileWriter.addPage(pdfReader.getPage(index))
    with open(target_file_path, 'wb') as file:
        pdfFileWriter.write(file)
    return target_file_path

def getPDFImage(file_path, output_path):
    target_file_path = deletePDF(file_path)
    doc = fitz.open(target_file_path)
    imgCount = 0
    for page in doc:
        if len(page.get_images()) > 0:
            # 遍历page.get_images()数组
            for item in page.get_images():
                imgCount += 1
                pix = fitz.Pixmap(doc, item[0])
                new_name = "img{}.png".format(imgCount)
                new_name = new_name.replace(':', '')
                #如果pix.n<5，可以直接存为png
                if pix.n < 3:
                    pix.save(os.path.join(output_path, new_name))
                # 否则先转换为CMYK
                else:
                    pix0 = fitz.Pixmap(fitz.csRGB, pix)
                    pix0.save(os.path.join(output_path, new_name))
                    pix0 = None
                # 释放资源
                pix = None
    print("提取了{}张图片".format(imgCount))
    doc.close()
    os.remove(target_file_path)