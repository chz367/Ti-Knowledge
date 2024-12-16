# -*- codeing = utf-8 -*-
# @Time :2022/8/26 下午5:10
# @Author:Alex
# @File :extract_knowledge.py
# @Software: PyCharm

def knowledge_abstract():
    resName = "../knowledge_result.txt"
    result = open(resName, 'w', encoding='utf-8')
    for line in open('../ScienceDirect_citations_1661499568690_1_100.txt', 'r').readlines():
        if line.__contains__('Abstract:'):
            print(line)
            result.write(line)
    for line in open('../ScienceDirect_citations_1661499646357_101-200.txt', 'r').readlines():
        if line.__contains__('Abstract:'):
            print(line)
            result.write(line)

extract_knowledge()