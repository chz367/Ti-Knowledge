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
获取文献摘要
"""
def getPMAbstract(file_path):
    filename = getText(file_path)
    f = open(filename, 'r', encoding='UTF-8')
    start_line = 0
    end_line = 0
    content = []
    regex1 = re.compile(r'^ABSTRACT$', re.IGNORECASE)
    regex2 = re.compile(r'^ARTICLE HISTORY$', re.IGNORECASE)
    for index, ele in enumerate(f.readlines()):
        content.append(ele)
        if regex1.search(ele.strip()):
            start_line = index + 1
        elif regex2.search(ele.strip()):
            end_line = index - 2
    abstract = ''
    f.seek(0, 0)
    for i in range(start_line, end_line+1):
        abstract += content[i].replace('\n', ' ').replace('\r', ' ')
    return abstract

"""
获取文献正文
"""
def getPMDetail(file_path):
    filename = getText(file_path)
    f = open(filename, 'r', encoding='UTF-8')
    start_line = 0
    end_line = 0
    res = ''
    regex1 = re.compile(r'^\d(.)*Introduction', re.IGNORECASE)
    regex2 = re.compile(r'^\d(.)*Conclusions', re.IGNORECASE)
    for index, ele in enumerate(f.readlines()):
        if regex1.search(ele):
            start_line = index
        elif regex2.search(ele):
            end_line = index
    f.seek(0, 0)
    for index, ele in enumerate(f.readlines()[start_line: end_line]):
        if len(ele.strip()) > 3:
            res += ele.replace('\n', ' ').replace('\r', ' ')
    return res

"""
抽取文章信息
"""
def getPMInfo(file_path):
    # 获取文章摘要
    abstract = getPMAbstract(file_path)
    # 拆分摘要句子
    token_abstract = sent_tokenize(abstract)
    # 获取文章正文内容
    content = sent_tokenize(getPMDetail(file_path))
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
def formPMTripleGroup(file_path):
    # 获取各指标句子
    extract_res = getPMInfo(file_path)
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
# 抽取文献正文信息
# """
# def getPMInfo(file_path):
#     abstract = getPMAbstract(file_path)
#     content = getPMDetail(file_path)
#     start = timeit.default_timer()
#     # 材料名称
#     f = open("WordBase\\powder.txt", 'r', encoding='utf-8')
#     powder_name = ''
#     for i in f.readlines():
#         regex = re.compile(r"\s(%s)\s" %i.strip())
#         if regex.search(abstract):
#             powder_name=i.strip()
#     print('材料名称:', powder_name)
#     f.close()
#     # 生产厂家(参照条件较少，正则表达式可能匹配不准确)
#     f = open("WordBase\\factory.txt", 'r', encoding='utf-8')
#     factory = ''
#     for i in f.readlines():
#         regex = re.compile(r"[(]produced(.)*?(%s)" % i.strip(), re.IGNORECASE)
#         try:
#             factory=regex.search(content).group()
#         except:
#             factory = []
#     print('生产厂家: ', factory)
#     f.close()
#     # 粉末形貌
#     powder_shape = ''
#     # 粒径分布
#     # 切分摘要
#     sear_sen = abstract.split('.')
#     f = open(r"WordBase\\particle_size_distribution.txt", 'r', encoding='utf-8')
#     particle_size_distribution = ''
#     for i in f.readlines():
#         for j in sear_sen:
#             if i.strip() in j:
#                 particle_size_distribution = j
#     f.close()
#     # 粉末加工方法
#     powder_work_method = ''
#     f = open(r"WordBase\\powder_work_method.txt", 'r', encoding='utf-8')
#     for i in f.readlines():
#         regex = re.compile(r'\s(%s)\s' %i.strip(), re.IGNORECASE)
#         if regex.search(abstract):
#             powder_work_method=i.strip()
#     f.close()
#     # 块体加工方法
#     block_work_method = ''
#     f = open(r"WordBase\\block_work_method.txt", 'r', encoding='utf-8')
#     for i in f.readlines():
#         regex = re.compile(r'(%s)' %i.strip(), re.IGNORECASE)
#         if regex.search(abstract):
#             block_work_method=i.strip()
#     f.close()
#     # 显微组织
#     microstructure = ''
#     # 抗拉强度
#     ab_sen = abstract.split('. ')
#     tensile_strength = []
#     f = open(r"WordBase\\uts.txt", "r", encoding='utf-8')
#     for i in f.readlines():
#         regex = re.compile(r'\s(%s)\s' %i.strip())
#         for j in ab_sen:
#             if regex.search(j.strip()):
#                 tensile_strength = j
#     f.close()
#     # 断裂延伸率
#     elongation = ''
#     # 显微硬度
#     microhardness = ''
#     f = open(r"WordBase\\microhardness.txt", "r", encoding='utf-8')
#     k1=0
#     for index, ele in enumerate(f.readlines()):
#         regex = re.compile(r"(%s)(.)*?(\d)+(\s)?[Hh][Vv]" %ele.strip(), re.IGNORECASE)
#         if regex.search(content):
#             if(k1==0):
#                 microhardness=regex.search(content).group().strip()
#             k1=1
#     f.close()
#     # 屈服强度
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