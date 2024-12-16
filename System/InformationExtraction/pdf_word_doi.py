# from pdf2docx import Converter
from docx import Document
from docx.oxml.ns import qn
import re
import textract
from pdf2docx import Converter
import os

def find_hyperlink_indoc(doc):
    xml_e = doc.element
    hyperlink_list = xml_e.findall('.//' + qn("w:hyperlink"))
    return hyperlink_list

def get_hyperlink_text(hyperlink_item):
    text = hyperlink_item.findall('.//' + qn("w:t"))[0].text
    return text

def set_hyperlink_text(hyperlink_item, text):
    hyperlink_item.findall('.//' + qn("w:t"))[0].text = text

def pdf2word(pdf_file):
    cv = Converter(pdf_file)
    pdf_file = pdf_file[:-4]
    cv.convert(pdf_file + '.docx', start=0, end=None)
    cv.close()
    return pdf_file + '.docx'
        
# 获取文章doi号
def get_doi(pdf_file, journal_type):
    doi = ''
    word_path = pdf2word(pdf_file)
    # 打开word文档
    document = Document(word_path)
    hl_list = find_hyperlink_indoc(document)
    if journal_type == 'ELSEVIER_NEW' or journal_type == 'CRYSTALS' or journal_type == 'MATERIALS_SCIENCE_FORUM' or journal_type == 'POWDER_METALLURGY':
        # 超链接类型的DOI
        for item in hl_list:
            regex = re.compile(r'^(http)?(s)?(://)?(.)*doi(.org/)?(.)*', re.IGNORECASE)
            if regex.search(get_hyperlink_text(item)):
                doi = regex.search(get_hyperlink_text(item)).group()
                if os.path.isfile(word_path):
                    os.remove(word_path)
                return get_hyperlink_text(item)

    elif journal_type == 'ELSEVIER_OLD' or journal_type == 'OPTO_ELECTRONIC_ADVANCES' or journal_type == 'MATERIALS_RESEARCH':
        # 将pdf转为txt
        # text = textract.process(pdf_file, method='pdfminer')
        text = textract.process(pdf_file)
        # 将文本内容写入txt
        file_handle = open(pdf_file[:-4] + '.txt', mode='wb')
        file_handle.write(text)
        file_handle.close()
        regex = re.compile(r'DOI:(.)*', re.IGNORECASE)
        f = open(pdf_file[:-4] + '.txt', 'r', encoding='UTF-8')
        for ele in f.readlines():
            if regex.search(ele.strip()):
                doi = regex.search(ele.strip()).group()
                break
        f.close()
        if os.path.isfile(pdf_file[:-4] + '.txt'):
            os.remove(pdf_file[:-4] + '.txt')
    if os.path.isfile(word_path):
        os.remove(word_path)    
    return doi