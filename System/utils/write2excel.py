# -*- coding:utf-8 -*-
# 导入xlwt模块
import xlwt
from tkinter import filedialog
import xlrd
from xlutils.copy import copy

def write2ExcelSingle(data):
    """单独写入数据
    Args:
        data (_type_): 要写入的数据，为二维数组
    """
    # 创建一个Workbook对象，编码encoding
    Excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 添加一个sheet工作表、sheet名命名为用户命名、cell_overwrite_ok=True 允许覆盖写
    table = Excel.add_sheet('Sheet1', cell_overwrite_ok=True)
    for l in range(data.shape[0]):
        for c in range(data.shape[1]):
            # table.write(行， 列，要写入的数据)
            table.write(l, c, data[l, c])
    files = [('Excel Files', '*.xlsx')]
    file_path = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    # 保存文件
    Excel.save(file_path)

def excelAppendData(filepath, data, sheet_name):
    """向Excel中追加数据
    Args:
        filepath (_type_): excel文件名
        data (_type_): 需要追加的数据,列表形式
        sheet_name (_type_): 表名
    """
    wb = xlrd.open_workbook(filepath, formatting_info=False)
    xwb = copy(wb)
    # 指定sheet，并获取sheet总行数
    sheet = xwb.get_sheet(sheet_name)
    rows = sheet.get_rows()
    lineNum = len(rows)
    for col in range(len(data)):
        sheet.write(lineNum, col, data[col])
    xwb.save(filepath)

def updateExcel(filepath, sheet_name, line, data):
    """更新excel数据
    Args:
        filepath (_type_): 文件路径
        sheet_name (_type_): 表单名
        line (_type_): 要更新的行
        data (_type_): 要更新的数据
    """
    oldWb = xlrd.open_workbook(filepath)
    newWb = copy(oldWb)
    newWs = newWb.get_sheet(sheet_name)
    for col in range(len(data)):
        newWs.write(line, col, data[col])
    newWb.save(filepath)
        
def judgeIfSame(filepath, content, sheet_name, data):
    """判断excel中标题列是否有相同数据
    Args:
        filepath (_type_): 文件路径
        content (_type_): 判断是否有相同内容
        sheet_name (_type_): 表名
        data (_type_): 需要写入的数据
    """
    worksheet = xlrd.open_workbook(filepath)
    sheet = worksheet.sheet_by_name(sheet_name)
    cols = sheet.col_values(0)[1:]
    if content in cols:
        # 如果有重复内容，则更新
        print('有重复内容')
        updateExcel(filepath, sheet_name, cols.index(content) + 1, data) 
    else:
        # 如果没有重复内容，则追加数据
        excelAppendData(filepath, data, sheet_name)
