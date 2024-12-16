import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from Information import InformationExtract
import xlrd
from ConnectSql import ConnectDataBase

class SearchPage(tk.Tk):

    def __init__(self, ifChinese):
        super().__init__()
        self.db = ConnectDataBase()
        self.cursor = self.db.cursor
        self.ifChinese = ifChinese
        self.setWindow()
        self.setWindowContent()
        self.setSearchContent()
    
    """
    设置窗口内容
    """
    def setWindow(self):
        self.geometry('900x700')
        self.title("面向Ti材料领域的知识基因提取及基因库构建系统" if self.ifChinese==True else 'Knowledge gene extraction and gene bank construction system for Ti material field')
        self.iconphoto(False, tk.PhotoImage(file='image\\system_icon\\sys_icon.png'))
        self.resizable(False, False)
    
    """
    设置窗体内容
    """
    def setWindowContent(self):
        # 添加画布
        self.myCanvas1 = Canvas(self, bg='#0065B3', height=200)
        # 去掉画布周围的白色边框
        self.myCanvas1.config(highlightthickness=0)
        # 画布位置
        self.myCanvas1.pack(side=TOP, anchor=NW, fill=X, expand=True)
        # 打开图片
        self.universityImage = Image.open('image\\system_icon\\university_white.jpeg')
        # 改变图片大小
        self.universityImage = self.universityImage.resize((30, 30))
        self.universityIcon = ImageTk.PhotoImage(self.universityImage)
        self.universityLabel = Label(self.myCanvas1, image=self.universityIcon, text='面向Ti材料领域的知识基因提取及基因库构建系统' if self.ifChinese==True else 'Knowledge gene extraction and gene bank construction system for Ti material field', \
            compound=LEFT, font=('华文仿宋' if self.ifChinese==True else 'Times New Roman', 15 if self.ifChinese==True else 10, 'bold'), bg='#0065B3', fg='white')
        self.universityLabel.place(relx=0.01, rely=0.01)
        # 找不到结果
        self.labelNotFound = Label(self.myCanvas1, text='找不到结果？直接' if self.ifChinese==True else 'No results? To', font=("华光标题宋_CNKI" if self.ifChinese==True else 'Times New Roman', 12), bg="#0065B3", foreground='white')
        self.labelNotFound.place(relx=0.63 if self.ifChinese==True else 0.64, rely=0.02)
        self.labelUpload = Label(self.myCanvas1, text='上传提取' if self.ifChinese==True else 'Extract', font=("华光标题宋_CNKI" if self.ifChinese==True else 'Times New Roman', 12, 'underline'), bg="#0065B3", foreground='#EBE615', cursor='hand2')
        self.labelUpload.place(relx=0.775 if self.ifChinese==True else 0.745, rely=0.02)
        self.labelUpload.bind('<Button-1>',lambda _: self.toExtract('#', self.ifChinese))
        # 添加返回按钮
        self.backLabel = Label(self.myCanvas1, text='返回上一页' if self.ifChinese==True else 'Return to previous page', font=('华光标题宋_CNKI' if self.ifChinese==True else 'Times New Roman', 12, 'underline'), bg='#0065B3', fg='#F2DEB0', cursor='hand2')
        self.backLabel.place(relx=0.88 if self.ifChinese==True else 0.83, rely=0.02)
        self.backLabel.bind('<Button-1>', self.toIndex)        
        # 内容检索
        self.labelSearch = Label(self.myCanvas1, text='材料论文库历史提取记录' if self.ifChinese==True else 'Historical extraction record of material paper library', font=('华光魏体_CNKI' if self.ifChinese==True else 'Times New Roman', 20, 'bold'), bg='#0065B3', foreground='white')
        self.labelSearch.place(relx=0.335 if self.ifChinese==True else 0.15, rely=0.30)
        # 默认显示所有提取记录列表，若没有相关提取记录，则显示空状态
        self.cursor.execute('SELECT * FROM material_knowledge_base m ORDER by m.update_time DESC')
        self.showExtractRecords(self.cursor.fetchall())
        
    def showSingleRecord(self, number,  title, doi, flag):
        """设置显示单条记录
            number: 记录编号
            title: 文献标题
            author: 文献作者
            doi: 文献doi
            flag: 是否显示滚动条
        """
        # 获取用户点击的记录内容
        eval_record = lambda x: (lambda p: self.toExtract(x, self.ifChinese))
        locals()['record'+str(number)] = Frame(self.resCanvas, relief='groove', bg='white' if number%2==0 else '#F0F0F0', width=880 if flag==True else 900, height=60)
        locals()['record'+str(number)].place(x=0, y=60*(number-1))
        locals()['messageImage'+str(number)] = Image.open('image\\system_icon\\message.png')
        locals()['messageImage'+str(number)] = locals()['messageImage'+str(number)].resize((60, 40))
        locals()['messageIcon'+str(number)] = ImageTk.PhotoImage(locals()['messageImage'+str(number)])
        locals()['messageLabel'+str(number)] = Label(locals()['record'+str(number)], image=locals()['messageIcon'+str(number)], bg='white' if number%2==0 else '#F0F0F0')
        locals()['messageLabel'+str(number)].image = locals()['messageIcon'+str(number)]
        locals()['messageLabel'+str(number)].place(relx=0.03, rely=0.15)
        locals()['messageTitleLabel' + str(number)] = Label(locals()['record'+str(number)], text=('标题：' if self.ifChinese==True else 'Title:')+ (title if len(title) < 55 else title[:55]+'...'), font=('华光标题宋_CNKI' if self.ifChinese==True else 'Times New Roman', 13), bg='white' if number%2==0 else '#F0F0F0', fg='#4F573E')
        locals()['messageTitleLabel' + str(number)].place(relx=0.18, rely=0.08)
        locals()['messageDOILabel' + str(number)] = Label(locals()['record'+str(number)], text=('DOI号：' if self.ifChinese==True else 'DOI:')+ doi, font=('华光标题宋_CNKI' if self.ifChinese==True else 'Times New Roman', 13), bg='white' if number%2==0 else '#F0F0F0', fg='#4F573E')
        locals()['messageDOILabel' + str(number)].place(relx=0.18, rely=0.5)
        # 点击查看详细信息按钮
        locals()['messageDetailButton' + str(number)] = Label(locals()['record'+str(number)], text='查看详情' if self.ifChinese==True else 'Detail', font=('华光标题宋_CNKI' if self.ifChinese==True else 'Times New Roman', 13, 'underline'), bg='white' if number%2==0 else '#F0F0F0', fg='#1457C8', cursor='hand2')
        locals()['messageDetailButton' + str(number)].place(relx=0.85, rely=0.3)
        locals()['messageDetailButton' + str(number)].bind('<Button-1>', eval_record(
            {
                'title': title,
                'doi': doi
            }
        ))
        self.resCanvas.create_window(0, 60*(number-1), window=locals()['record'+str(number)], anchor='nw', width=880 if flag==True else 900)
        
    """
    设置显示所有提取记录
    """
    def showExtractRecords(self, data):
        # 从云DB中查找有无相关记录，若没有，则显示空状态
        try:
            self.resCanvas.destroy()
        except:
            pass
        self.resCanvas = Canvas(self, bg='white', height=700)
        self.resCanvas.config(highlightthickness=0)
        self.resCanvas.pack(side=TOP, anchor=NW, fill=BOTH, expand=True)
        if len(data) == 0:
            self.emptyImage = Image.open('image\\system_icon\\empty.png')
            self.emptyImage = self.emptyImage.resize((200, 200))
            self.emptyIcon = ImageTk.PhotoImage(self.emptyImage)
            self.emptyLabel = Label(self.resCanvas, image=self.emptyIcon, bg='white')
            self.emptyLabel.place(x=350, y=130)
        else:
            # 不添加滚动条，直接显示
            for index, rec in enumerate(data):
                self.showSingleRecord(index+1, rec[1], rec[2], flag=True if len(data) > 8 else False)
            if len(data) > 8:
            # 添加滚动条
                self.myScrollbar = Scrollbar(self.resCanvas, orient=VERTICAL, width=20)
                self.myScrollbar.place(x=880, y=0, height=self.winfo_width()-400)
                self.resCanvas.config(yscrollcommand=self.myScrollbar.set)
                self.myScrollbar.config(command=self.resCanvas.yview)
                self.resCanvas.config(scrollregion=self.resCanvas.bbox('all'))
                self.resCanvas.bind_all("<MouseWheel>", self.wheel)
            else:
                try:
                    self.myScrollbar.destroy()
                except:
                    pass
                
    
    def wheel(self, event):
        """鼠标滚轮事件
        """
        number = int(-(event.delta)//120)
        self.resCanvas.yview_scroll(number, 'units') 
    
    """
    设置搜索功能
    """
    def setSearchContent(self):
        # 设置下拉框
        self.selectCombobox = ttk.Combobox(self.myCanvas1, height=3, width=30, justify='center', state='normal', \
            font=('楷体' if self.ifChinese==True else 'Times New Roman', 13), cursor='hand2', values=['标题', '作者', '标题关键字'] if self.ifChinese==True else ['Title', 'Author', 'Title Keywords'])
        self.selectCombobox.place(relx=0.04, rely=0.56, width=120, height=35.6)
        self.selectCombobox.set('标题' if self.ifChinese else 'Title')
        # 设置输入框
        self.placeValue = tk.StringVar()
        self.placeValue.set('Please enter content...')
        self.inputItem = Entry(self.myCanvas1, font=("Times New Roman", 14), textvariable=self.placeValue)
        self.inputItem.place(relx=0.174, rely=0.56, width=600, height=35)
        # 清空文本框默认值
        self.inputItem.bind('<Button-1>', self.clearAll)
        # 设置带图标的button按钮
        self.searImage = Image.open("image\\system_icon\\search_item.png")
        self.searImage = self.searImage.resize((23, 23))
        self.searIcon = ImageTk.PhotoImage(self.searImage)
        # compound:对齐方式
        self.btnSearch = Button(self.myCanvas1, text='搜索' if self.ifChinese==True else 'Search', \
            command=self.toSearchArticle, bg='#ffffff', \
            fg='#333333', font=("宋体" if self.ifChinese==True else 'Times New Roman', 14, 'bold'), \
            image=self.searIcon, compound=LEFT)
        self.btnSearch.place(relx=0.843, rely=0.56, width=100, height=35.6)
        
    """
    开始搜索内容
    """
    def toSearchArticle(self):
        # 获取下拉框的值, 如果用户选择的是标题
        print(self.inputItem.get())
        if self.selectCombobox.get() == '标题' or self.selectCombobox.get() == 'Title':
            self.cursor.execute('SELECT * FROM material_knowledge_base m WHERE m.title={}'.format('"'+self.inputItem.get()+'"'))
        elif self.selectCombobox.get() == '作者' or self.selectCombobox.get() == 'Author':
            self.cursor.execute('SELECT * FROM material_knowledge_base m WHERE m.author={}'.format('"'+self.inputItem.get()+'"'))
        elif self.selectCombobox.get() == '标题关键字' or self.selectCombobox.get() == 'Title Keywords':
            self.cursor.execute('SELECT * FROM material_knowledge_base m WHERE INSTR(m.title, {})'.format('"'+self.inputItem.get()+'"'))
        searchRec = self.cursor.fetchall()
        # 提示用户无相关记录
        if len(searchRec) == 0:
            showinfo(title='提示' if self.ifChinese==True else 'Prompt', message='无相关内容' if self.ifChinese==True else 'No Result!')
            # 查找数据库内容是否为空，若为空，则显示空图片，否则，显示相关记录内容
            self.cursor.execute('SELECT * FROM material_knowledge_base')
            allRec = self.cursor.fetchall()
            self.showExtractRecords(allRec)
        else:
            self.showExtractRecords(searchRec)

    """
    清空搜索框的默认值
    """   
    def clearAll(self, event):
        if self.inputItem.get() == 'Please enter content...':
            self.placeValue.set('')
        try:
            self.emptyLabel.config(image='', text='')
            self.extractLabel.config(text='')
        except:
            print(event)
    
    """
    跳转至信息抽取界面
    """
    def toExtract(self, event, ifChinese):
        print(event)  
        self.db.close_connect()
        self.destroy()
        # 参数为文献名 + 文献DOI
        InformationExtract(event, ifChinese)
    
    """跳转至指标修改界面
    """
    def toIndex(self, event):
        self.db.close_connect()
        self.destroy()
        from indexOperate import IndexAlter
        IndexAlter(self.ifChinese)