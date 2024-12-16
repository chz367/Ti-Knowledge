# -*- coding = utf-8 -*-
import os
import sys
from textwrap import wrap
# 获取文件目录
curPath = os.path.abspath(os.path.dirname(__file__))
# 获取项目根路径，内容为当前项目的名字
rootPath = curPath[:curPath.find(os.getcwd().split('\\')[-1]+"\\")+len(os.getcwd().split('\\')[-1]+"\\")]
sys.path.append(rootPath)
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from indexOperate import IndexAlter
from ConnectSql import ConnectDataBase


"""
系统首界面
"""
class SystemMain(tk.Tk):
    
    def __init__(self, ifChinese):
        super().__init__()
        # 连接数据库
        self.db = ConnectDataBase()
        self.cursor = self.db.cursor
        # 中英文切换标志
        self.ifChinese = ifChinese
        self.langVal = StringVar()
        self.langVal.set('中文' if ifChinese==True else 'English')
        # 字体颜色
        self.titleColor = '#2B3C6F'
        self.infoColor = '#031A2B'
        self.setWindow()
        self.resizable(False, False)
        self.setWindowLabel(self.getPaperNumber())
        self.setSystemLanguage()
        self.setWindowButton()
    
    """
    获取所有文件的数量
    """    
    def getPaperNumber(self):
        # 调用数据库数据获取已解析的文件数量
        self.cursor.execute('select * from material_knowledge_base;')
        return len(self.cursor.fetchall())

    """
    设置窗口大小、标题、窗口图标
    """    
    def setWindow(self):
        self.geometry('750x500')
        self.title("面向Ti材料领域的知识基因提取及基因库构建系统" if self.ifChinese == True else 'Knowledge gene extraction and gene bank construction system for Ti material field')
        self.iconphoto(False, tk.PhotoImage(file='image\\system_icon\\sys_icon.png'))     
    
    """
    设置系统语言
    """
    def setSystemLanguage(self):
        try:
            self.languageLabel.destroy()
            self.languageCombobox.destroy()
        except:
            pass
        # 系统语言切换，在右上角设置
        self.languageLabel = Label(self, text='语言:' if self.ifChinese == True else 'Language:', font=('华文新魏' if self.ifChinese==True else 'Roboto Slab', 14))
        self.languageLabel.place(relx=0.73 if self.ifChinese == True else 0.675, rely=0.03)
        self.selectLanguage = ['中文', '英文'] if self.ifChinese == True else ['Chinese', 'English']
        self.languageCombobox = ttk.Combobox(master=self, width=8, state='readonly', cursor='hand2', \
            font=('华文新魏' if self.ifChinese==True else 'Roboto Slab', 14), values= self.selectLanguage, textvariable=self.langVal)
        self.languageCombobox.place(relx=0.81, rely=0.03)
        self.languageCombobox.bind('<<ComboboxSelected>>', self.changeLanguage)

    
    """
    设置窗口标签等内容
    """
    def setWindowLabel(self, paperNumber):
        # 设置画布
        self.systemCanvas = Canvas(self, bg='#f0f0f0', height=self.winfo_height(), width=self.winfo_width())
        self.systemCanvas.config(highlightthickness=0)
        self.systemCanvas.place(relx=0, rely=0)
        # 系统图片
        # 打开图片
        self.image = Image.open("image\\system_icon\\university_blue.png")
        # 改变图片大小
        self.image = self.image.resize((180, 180))
        self.pic = ImageTk.PhotoImage(self.image)
        # 添加画布
        self.myCanvas = Canvas(self.systemCanvas, bg='#f0f0f0', height=400, width=400)
        # 画布位置
        self.myCanvas.place(relx=0.116, rely=0.335)    
        # 画布上创建图像
        self.myCanvas.create_image(0, 0, image=self.pic, anchor='nw')
        # 图像位置
        self.myCanvas.place(relx=0.116, rely=0.335)
        self.myCanvas.image = self.pic
        # 系统标题
        self.labelName = Label(self.systemCanvas, text='面向Ti材料领域的知识基因提取及基因库构建系统' if self.ifChinese == True else 'Knowledge gene extraction and gene bank construction system for Ti material field',
                        font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', \
                            20 if self.ifChinese == True else 18, \
                            'normal' if self.ifChinese == True else 'bold'), 
                        fg=self.titleColor,
                        wraplength=1000 if self.ifChinese == True else 700        
                        )
        self.labelName.place(relx=0.1 if self.ifChinese==True  else 0.03, rely=0.16)
        if self.ifChinese == True:
            self.enLabelName = Label(self.systemCanvas, text='Knowledge gene extraction and gene bank construction system for material domain',\
                font=('Book Antiqua', 12, 'bold'), fg=self.titleColor)
            self.enLabelName.place(relx=0.095, rely=0.23)
        # 软件信息
        self.swInfo = Label(self.systemCanvas, text='系统信息简介' if self.ifChinese==True else 'System Information Introduction', font=('华文新魏' if self.ifChinese==True else 'Book Antiqua', 15), fg=self.infoColor)
        self.swInfo.place(relx=0.406, rely=0.326 if self.ifChinese==True else 0.296)
        # 软件版本号
        self.labelVersion = Label(self.systemCanvas, text='软件版本号：' if self.ifChinese==True else 'Software Version:', font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', 15), fg=self.infoColor)
        self.labelVersion.place(relx=0.406, rely=0.426 if self.ifChinese==True else 0.376)
        self.labelVersionNumber = Label(self.systemCanvas, text='Version 2.0.1', font=("Book Antiqua", 15 if self.ifChinese==True else 14), fg=self.infoColor)
        self.labelVersionNumber.place(relx=0.56 if self.ifChinese==True else 0.625, rely=0.426 if self.ifChinese==True else 0.376)
        # 软件功能简介
        self.labelFunc = Label(self.systemCanvas, text='软件功能简介：' if self.ifChinese==True else 'Features:', font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', 15), fg=self.infoColor)
        self.labelFunc.place(relx=0.406, rely=0.526 if self.ifChinese==True else 0.456)
        self.labelFuncDesc = Label(self.systemCanvas, text='本系统用于抽取材料文献中相关性能指标，提高科研效率。' if self.ifChinese==True else 'This system is used to extract relevant performance indexes from materials and literature, and improve scientific research efficiency.', font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', 15 if self.ifChinese==True else 14), \
            wraplength=260 if self.ifChinese==True else 320, fg=self.infoColor, justify='left')
        self.labelFuncDesc.place(relx=0.58 if self.ifChinese==True else 0.525, rely=0.526 if self.ifChinese==True else 0.456)
        # 论文库数据量
        self.labelNumTip = Label(self.systemCanvas, text='论文库数据量：' if self.ifChinese==True else 'Data volume of paper database:', font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', 15), fg=self.infoColor)
        self.labelNumTip.place(relx=0.406, rely=0.646 if self.ifChinese==True else 0.666)
        self.labelNum = Label(self.systemCanvas, text=str(paperNumber)+('条' if self.ifChinese==True else ''), font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', 15), fg=self.infoColor)
        self.labelNum.place(relx=0.58 if self.ifChinese==True else 0.79, rely=0.646 if self.ifChinese==True else 0.666)
        # 版权信息
        self.labelName = Label(self.systemCanvas, text='Copyright © 2022 K&D Group of USTB.All Rights Reserved.', font=("Book Antiqua", 13), fg='#A6A9AA')
        self.labelName.place(relx=0.230, rely=0.923)


    """
    改变系统语言
    """
    def changeLanguage(self, event):
        print('当前选择的语言是:', self.languageCombobox.get())
        if self.languageCombobox.get().strip() == '英文' or self.languageCombobox.get().strip() == 'English':
            # 将系统设置为英文
            self.ifChinese = False
            self.langVal.set('English')
            try:
                self.systemCanvas.destroy()
            except:
                pass
            self.setWindow()
            self.setWindowLabel(self.getPaperNumber())
            self.enLabelName.destroy()
            self.setSystemLanguage()
            self.setWindowButton()
        elif self.languageCombobox.get().strip() == '中文' or self.languageCombobox.get().strip() == 'Chinese':
            # 将系统设置为中文
            self.ifChinese = True
            self.langVal.set('中文')
            try:
                self.systemCanvas.destroy()
            except:
                pass
            self.setWindow()
            self.setWindowLabel(self.getPaperNumber())
            self.setSystemLanguage()
            self.setWindowButton()
            
    """
    设置窗口按钮，用于跳转至下一页
    """
    def setWindowButton(self):
        self.btnBegin = Button(self.systemCanvas, bg='#2D5A88', fg='white', text='开始提取' if self.ifChinese==True else 'Start', command=self.toSearchPage, \
            font=("华文新魏" if self.ifChinese==True else 'Book Antiqua', 15, 'bold'))
        self.btnBegin.place(relx=0.55, rely=0.756, relwidth=0.234, relheight=0.073)

    """
    跳转至搜索界面
    """
    def toSearchPage(self):
        # 关闭数据库连接
        self.db.close_connect()
        self.destroy()
        # 添加第二页
        IndexAlter(self.ifChinese)
