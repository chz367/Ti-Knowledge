from genericpath import isfile
from PyPDF2 import PdfFileReader as pdf_read
import sys
import textract
import re
import os

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
def getArticleTitle(file_path, journal_type):
    with open(file_path, 'rb') as f:
        pdf = pdf_read(f, strict=False)
        #检索文档中存在的文本大纲,返回的对象是一个嵌套的列表
        # ELSEVIER_NEW/CRYSTALS
        if pdf.getDocumentInfo().title != None and (journal_type == 'ELSEVIER_NEW' or journal_type == 'CRYSTALS'):
            return pdf.getDocumentInfo().title
        # ELSEVIER_OLD
        elif journal_type == 'ELSEVIER_OLD':
            return pdf.getOutlines()[0]['/Title']
        # MATERIALS_RESEARCH
        elif journal_type == 'MATERIALS_RESEARCH':
            if pdf.getDocumentInfo().title != None:
                return pdf.getDocumentInfo().title
            else:
                # 将文章转换为txt
                # text = textract.process(file_path, method='pdfminer')
                text = textract.process(file_path)
                file_handle=open(file_path[:-4] + '.txt', mode='wb')
                file_handle.write(text)
                file_handle.close()
                # 读取txt内容
                f = open(file_path[:-4]+'.txt', 'r', encoding='UTF-8')
                # 匹配作者所在那一行
                start_line = 0
                end_line = 0
                content = []
                title = ''
                for index, ele in enumerate(f.readlines()):
                    content.append(ele.replace('\n', ' ').replace('\r', ''))
                    regex = re.compile(r"((.)*[0-9],)+")
                    if regex.search(ele.strip()):
                        end_line = index
                        break
                for index, ele in enumerate(reversed(content)):
                    if ele.strip() == '':
                        start_line = len(content) - index
                        break
                for i in range(start_line, end_line):
                    title += content[i]
                f.close()
                # 删除过程文件
                if os.path.isfile(file_path[:-4]+'.txt'):
                    os.remove(file_path[:-4]+'.txt')
                return title
        # POWDER_METALLURGY
        elif journal_type == 'POWDER_METALLURGY':
            # text = textract.process(file_path, method='pdfminer')
            text = textract.process(file_path)
            file_handle=open(file_path[:-4] + '.txt', mode='wb')
            file_handle.write(text)
            file_handle.close()
            # 读取txt内容
            f = open(file_path[:-4]+'.txt', 'r', encoding='UTF-8')
            start_line = 0
            end_line = 0
            empty_num = 0
            content = []
            title = ''
            for index, ele in enumerate(f.readlines()):
                regex = re.compile(r"ISSN:(.)*")
                if regex.search(ele.strip()):
                    start_line = index
                    break
            f.close()
            f = open(file_path[:-4]+'.txt', 'r', encoding='UTF-8')
            for index, ele in enumerate(f.readlines()[start_line:]):
                content.append(ele.replace('\n', '').replace('\r', ''))
                if ele.strip() == '':
                    empty_num += 1
                if empty_num == 2:
                    end_line = index + start_line
                    break
            for i in range(1, len(content)):
                if len(content[i].strip()) != 0:
                    title += content[i]
            f.close()
            # 删除过程文件
            if os.path.isfile(file_path[:-4]+'.txt'):
                os.remove(file_path[:-4]+'.txt')
            return title
        # OPTO_ELECTRONIC_ADVANCES
        elif journal_type == 'OPTO_ELECTRONIC_ADVANCES':
            # text = textract.process(file_path, method='pdfminer')
            text = textract.process(file_path)
            file_handle=open(file_path[:-4] + '.txt', mode='wb')
            file_handle.write(text)
            file_handle.close()
            # 读取txt内容
            f = open(file_path[:-4]+'.txt', 'r', encoding='UTF-8')
            start_line = 0
            end_line = 0
            empty_num = 0
            content = []
            title = ''
            for index, ele in enumerate(f.readlines()):
                content.append(ele.replace('\n', '').replace('\r', ''))
                regex = re.compile(r'(^[A-Za-z]?[A-Za-z\s]+[0-9,])+')
                if regex.search(ele.strip()):
                    end_line = index
                    break
            for index, ele in enumerate(reversed(content)):
                if ele.strip() == '':
                    empty_num += 1
                if empty_num == 2:
                    start_line = len(content) - index
                    break
            for i in range(start_line, end_line):
                if len(content[i].strip())!=0:
                    title += content[i]
            f.close()
            # 删除过程文件
            if os.path.isfile(file_path[:-4]+'.txt'):
                os.remove(file_path[:-4]+'.txt') 
            return title
        elif journal_type == 'MATERIALS_SCIENCE_FORUM':
            # text = textract.process(file_path, method='pdfminer')
            text = textract.process(file_path)
            file_handle=open(file_path[:-4] + '.txt', mode='wb')
            file_handle.write(text)
            file_handle.close()
            f = open(file_path[:-4]+'.txt', 'r', encoding='UTF-8')
            start_line = 0
            end_line = 0
            title = ''
            # 匹配开始行，带有时间标志
            for index, ele in enumerate(f.readlines()):
                regex = re.compile(r'[0-9]{2}:[0-9]{2}:[0-9]{2}\)')
                if regex.search(ele.strip()):
                    start_line = index + 1
                    break
            f.seek(0, 0)
            for index, ele in enumerate(f.readlines()):
                regex = re.compile(r'([A-Za-z\s]+[0-9],[a-z\s]?[\*]?[,]?)+')
                if regex.search(ele.strip()):
                    end_line = index - 1
                    break
            f.seek(0, 0)
            for index, ele in enumerate(f.readlines()[start_line: end_line]):
                if len(ele.strip()) != 0:
                    title += ele.replace('\n', '').replace('\r', '')
            f.close()
            # 删除过程文件
            if os.path.isfile(file_path[:-4]+'.txt'):
                os.remove(file_path[:-4]+'.txt')             
            return title