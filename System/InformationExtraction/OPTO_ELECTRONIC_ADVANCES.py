import textract
import re
import os
import sys
# 获取文件目录
curPath = os.path.abspath(os.path.dirname(__file__))
# 获取项目根路径，内容为当前项目的名字
rootPath = curPath[:curPath.find(os.getcwd().split('\\')[-1]+"\\")+len(os.getcwd().split('\\')[-1]+"\\")]
sys.path.append(rootPath)
from SystemPages.ConnectSql import ConnectDataBase
from nltk.tokenize import sent_tokenize

# 连接数据库
db = ConnectDataBase()
cursor = db.cursor

"""
将pdf文件转换为txt文件
"""
def getText(file_path):
    # text = textract.process(file_path + ".pdf", method='pdfminer')
    text = textract.process(file_path + ".pdf")
    # 将文本内容写入txt
    file_handle=open(file_path + '.txt',mode='wb')
    file_handle.write(text)
    file_handle.close()
    filename = file_path + '.txt'
    return filename

"""
获取文献摘要信息
"""
def getOptoAbstract(file_path):
    filename = getText(file_path)
    f = open(filename, 'r', encoding='UTF-8')
    keywords_line = 0
    blankline = 0
    abstract = []
    res = ''
    for index, ele in enumerate(f.readlines()):
        if 'Keywords' in ele.strip():
            keywords_line = index
            break
    f.close()
    f = open(filename, 'r', encoding='UTF-8')
    for index, ele in enumerate(f.readlines()[keywords_line-1:1:-1]):
        if ele.strip() == '':
            blankline += 1
            if blankline == 2:
                break;
        if ele.strip() != '':
            abstract.append(ele.strip())
    for ele in reversed(abstract):
        res += ele
    return res

"""
获取文献正文内容信息
"""
def getOptoDetail(file_path):
    filename = getText(file_path)
    # 获取文件对象
    f = open(filename, 'r', encoding='UTF-8')
    line_scope = []
    for index, ele in enumerate(f.readlines()):
        if ele.strip() == 'Experimental':
            line_scope.append(index)
        if ele.strip() == 'Conclusions':
            line_scope.append(index)
            break
    f.close()
    f = open(filename, 'r', encoding='UTF-8')
    line_value = ''
    for item in f.readlines()[line_scope[0]:line_scope[1] + 1]:
        if len(item.strip()) > 5:
            line_value += item.strip()
    f.close()
    return line_value

"""
抽取文章信息
"""
def getOptoInfo(file_path):
    # 获取文章摘要
    abstract = getOptoAbstract(file_path)
    # 拆分摘要句子
    token_abstract = sent_tokenize(abstract)
    # 获取文章正文内容
    content = sent_tokenize(getOptoDetail(file_path))
    # 将全文作为信息提取内容
    content.extend(token_abstract)
    # 获取数据库中数据
    cursor.execute('SELECT * from word_base w WHERE w.index_name="powder_name"')
    powder_index = [item[2] for item in cursor.fetchall()]
    # 粉末名称
    powder_name = []
    for item in powder_index:
        regex = re.compile(r"\s(%s)\s" % item.strip(), re.IGNORECASE)
        if regex.search(abstract):
            powder_name.append(item.strip())
    # 匹配指标
    # 获取所有的指标
    cursor.execute('SELECT * FROM index_base')
    all_index = [item[1] for item in cursor.fetchall()]
    # 保存指标提取结果
    index_res = []
    finally_res = []
    for index in all_index:
        # 去掉粉末名称指标，已经知道
        if index != 'powder_name':
            cursor.execute('SELECT * From word_base w WHERE w.index_name={}'.format('"' + index + '"'))
            item_index = [item[2] for item in cursor.fetchall()]
            # 循环遍历句子
            for sen in content:
                for powder in powder_name:
                    for item in item_index:
                        # 如果粉末名和指标均包含
                        regex_name = re.compile(r"\s(%s)\s" % powder.strip(), re.IGNORECASE)
                        regex_item = re.compile(r"\s(%s)[.,\s]?" % item.strip(), re.IGNORECASE)
                        
                        if (regex_name.search(sen)) and (regex_item.search(sen)):
                            index_res.append(
                                {
                                    'powder_name': powder,
                                    'index_name': index,
                                    'index_sen': sen
                                }
                            )
    # 列表元素去重
    [finally_res.append(item) for item in index_res if item not in finally_res]
    return finally_res

"""
形成三元组信息
"""
def formOptoTripleGroup(file_path):
    # 获取各指标句子
    extract_res = getOptoInfo(file_path)
    tripleGroup = []
    # 以各指标句子为依据形成三元组
    for item in extract_res:
        # 从数据库中查找匹配规则
        cursor.execute('SELECT * From rule_base r WHERE r.index_name={}'.format('"' + item['index_name'] + '"'))
        # 找到该指标的所有规则
        index_res = cursor.fetchall()
        # 根据规则在句子中匹配，形成三元组
        for rule in index_res:
            if '%s' in rule[2]:
                # 从数据库中获取词库内容，进行词语匹配
                cursor.execute('SELECT * FROM word_base w WHERE w.index_name={}'.format('"' + item['index_name'] + '"'))
                word_res = cursor.fetchall()
                for word in word_res:
                    rule_res = re.compile('{}'.format(rule[2]) %word[2].strip(), re.IGNORECASE)
                    if rule_res.search(item['index_sen']):
                        tripleGroup.append(
                            {
                                'powder_name': item['powder_name'],
                                'index_name': item['index_name'],
                                'index_sen': item['index_sen'],
                                'triple_res': item['powder_name'] + '--' + item['index_name'] + '--' + rule_res.search(item['index_sen']).group().strip()
                            }
                        )
            elif '\d' in rule[2]:
                rule_res = re.compile('{}'.format(rule[2]), re.IGNORECASE)
                if rule_res.search(item['index_sen']):
                    tripleGroup.append(
                        {
                            'powder_name': item['powder_name'],
                            'index_name': item['index_name'],
                            'index_sen': item['index_sen'],
                            'triple_res': item['powder_name'] + '--' + item['index_name'] + '--' + rule_res.search(item['index_sen']).group().strip()
                        }
                    ) 
    return tripleGroup

# """
# 抽取正文内容信息
# """
# def getOptoInfo(file_path):
#     abstract = getOptoAbstract(file_path)
#     content = getOptoDetail(file_path)
#     start = timeit.default_timer()
#     # 获取材料名称
#     f = open(r"WordBase\\powder.txt", 'r', encoding='UTF-8')
#     powder_name = ''
#     for i in f.readlines():
#         regex = re.compile(r"\s(%s)\s" % i.strip())
#         if regex.search(abstract):
#             powder_name = regex.search(abstract).group().strip()
#             break
#     f.close()
#     # 获取生产厂家
#     f = open(r"WordBase\\factory.txt", 'r', encoding='UTF-8')
#     factory = ''
#     for i in f.readlines():
#         regex = re.compile(r"\.\s(.*)(%s)" % i.strip())
#         if regex.search(content):
#             factory = regex.search(content).group().strip()[1:]
#             break
#     f.close()
#     # 粉末形貌
#     f = open(r"WordBase\\powder_shape.txt", 'r', encoding='UTF-8')
#     powder_shape = []
#     for i in f.readlines():
#         regex = re.compile(r"\s?(%s)\s?" %i.strip())
#         if regex.search(abstract):
#             powder_shape.append(regex.search(abstract).group().strip())
#     f.close()
#     # 粒径分布
#     particle_size_distribution = ''
#     # 粉末加工方法
#     f = open(r"WordBase\\powder_work_method.txt", 'r', encoding='UTF-8')
#     powder_work_method = []
#     for i in f.readlines():
#         regex = re.compile(r"\s?(%s)\s?" %i.strip())
#         if regex.search(abstract):
#             powder_work_method.append(regex.search(abstract).group().strip())
#     f.close()
#     # 块体加工方法
#     block_work_method = []
#     f = open(r"WordBase\\block_work_method.txt", 'r', encoding='UTF-8')
#     for i in f.readlines():
#         regex = re.compile(r"\s?(%s)\s?" %i.strip())
#         if regex.search(content):
#             block_work_method.append(regex.search(content).group().strip())
#     f.close()
#     # 显微组织
#     microstructure = []
#     f = open(r"WordBase\\microstructure.txt", 'r', encoding='UTF-8')
#     for i in f.readlines():
#         regex = re.compile(r"\s?(%s)\s?" %i.strip())
#         if regex.search(content):
#             microstructure.append(regex.search(content).group().strip())
#     f.close()
#     # 抗拉强度
#     tensile_strength = []
#     try:
#         regex = re.compile(r"\d(.)*MPa")
#         tensile_strength.append(regex.search(abstract).group().strip())
#     except:
#         tensile_strength = []
#     # 断裂延伸率
#     elongation = []
#     try:
#         regex = re.compile(r"[0-9]*[.]?[0-9]*%(.)*elongation", re.IGNORECASE)
#         elongation.append(regex.search(abstract).group().strip())
#     except:
#         elongation = []
#     # 显微硬度
#     microhardness = ''
#     # 屈服硬度
#     yield_strength = ''
#     # 抗压强度
#     compressive_strength = ''
#     end=timeit.default_timer()
#     print('Running time: %s Seconds' %(end - start))
    
#     return {
#         'powderName': powder_name,
#         'factory': factory,
#         'particleSizeDistribution': particle_size_distribution,
#         'powderShape': powder_shape,
#         'powderWorkMethod': powder_work_method,
#         'blockWorkMethod': block_work_method,
#         'microstructure': microstructure,
#         'tensileStrength': tensile_strength,
#         'elongation': elongation,
#         'microhardness': microhardness,
#         'yieldStrength': yield_strength,
#         'compressiveStrength': compressive_strength
#     }
