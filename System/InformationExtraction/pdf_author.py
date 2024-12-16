import textract
import re
import os

# 将pdf转换为word
def getArticleAuthor(file_path):
    # text = textract.process(file_path, method='pdfminer')
    text = textract.process(file_path)
    file_handle=open(file_path[:-4] + '.txt', mode='wb')
    file_handle.write(text)
    file_handle.close()   
    # 读取txt内容
    f = open(file_path[:-4]+'.txt', 'r', encoding='UTF-8')
    for line in f.readlines():
        regex = re.compile(r"(^[A-Z](.)*[⁎∗*](.)*)+")
        if regex.search(line.strip()):
            print(line)
            break
    if os.path.isfile(file_path[:-4]+'.txt'):
        f.close()
        os.remove(file_path[:-4]+'.txt')