# coding: utf-8

import wx
import xlrd
import wx.grid
from untitled.Kmeans import KMeans_Main
#import DBN
from Lasso_PLS import Lasso_PLS_Main
from DBN import DBN_PLS_Main
from numpy import *
from KNN import KNN_Main
from PLS import PLS_Main
import os

class MyFrame(wx.Frame):
    def __init__(self, wheretogo,parent=None, id=-1, title='中医药数据分析平台'):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))
        setImg = wx.Image('school.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        setIcon = wx.Icon(setImg)
        font1 = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT)
        self.wheretogo=wheretogo
        self.SetIcon(setIcon)
        self.CenterOnScreen()
        self.string_choose1 = []
        self.string_choose2 = []
        self.choose=0
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT)
        panel = wx.Panel(self)
        statusbar = self.CreateStatusBar()
        statusbar.SetStatusText('版权所有:计算机学院B313')
        statusbar.SetFont(font1)
        self.t1 = wx.TextCtrl(panel, pos=(30, 30), size=(530, 30))
        self.t1.SetFont(font)
        self.t3 = wx.ListBox(panel, pos=(450, 110), style = wx.LB_MULTIPLE, size=(110, 360))
        self.t4 = wx.ListBox(panel, pos=(630, 110), size=(110, 160), style = wx.LB_MULTIPLE)
        self.t5 = wx.ListBox(panel, pos=(630, 310), size=(110, 160), style = wx.LB_MULTIPLE)
        self.grid = wx.grid.Grid(panel,size = (400, 440), pos=(30, 110))
        self.grid.CreateGrid(12000,30)
        self.OpenButton = wx.Button(panel, -1, '打开文件(EXCEL)',pos=(600, 30), size=(140, 30))
        self.ChooseButton = wx.Button(panel, -1, '模型参数设置', pos=(580, 480), size=(160, 70))
        self.ChooseButton.SetFont(font)
        self.ZhuanHuan1 = wx.Button(panel, -1, '->', pos=(580, 180), size=(30, 30))
        self.ZhuanHuan2 = wx.Button(panel, -1, '->', pos=(580, 350), size=(30, 30))
        self.Bind(wx.EVT_BUTTON, self.Open, self.OpenButton)
        self.Bind(wx.EVT_BUTTON, self.show1, self.ZhuanHuan1)
        self.Bind(wx.EVT_BUTTON, self.show2, self.ZhuanHuan2)
        self.ChooseButton.Bind(wx.EVT_BUTTON, self.judge)
        self.string_choose3 = []
        lbl1 = wx.StaticText(panel, -1, label='数据显示', style=wx.ALIGN_LEFT, pos=(30, 80), size=(40, 20))
        lbl1.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT, False, '宋体'))
        lbl2 = wx.StaticText(panel, -1, label='变量', style=wx.ALIGN_LEFT, pos=(450, 80), size=(40, 20))
        lbl2.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT))
        lbl3 = wx.StaticText(panel, -1, label='自变量', style=wx.ALIGN_LEFT, pos=(630, 80), size=(40, 20))
        lbl3.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT))
        lbl4 = wx.StaticText(panel, -1, label='因变量', style=wx.ALIGN_LEFT, pos=(630, 290), size=(40, 20))
        lbl4.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.LIGHT))
        lblList = ['首行保留', '首行去除']
        rbox = wx.RadioBox(panel, label='Choose', pos=(450, 470), choices=lblList,
                                majorDimension=1, size=(110,80), style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_LISTBOX, self.LB1, self.t3)
        self.Bind(wx.EVT_LISTBOX, self.LB2, self.t4)
        self.Bind(wx.EVT_LISTBOX, self.LB3, self.t5)
        if self.wheretogo==4:
            self.ZhuanHuan2.Enable(False)
    def judge(self,event):
        if (self.t4.GetCount()==0 and self.wheretogo==4) or ((self.t4.GetCount()==0 or self.t5.GetCount()==0)and self.wheretogo!=4):
            wx.MessageBox("缺少因变量或自变量", "警告", wx.OK | wx.ICON_INFORMATION)
        else:
            self.Close()
            if self.wheretogo==1:#PLS
                PLS_Main.main()
            if self.wheretogo==2:#Lasso_PLS
                Lasso_PLS_Main.main()
            if self.wheretogo==3:#DBN
                DBN_PLS_Main.main()
            if self.wheretogo==4:#Kmeans
                KMeans_Main.main(self.data)
            if self.wheretogo==5:#KNN
                KNN_Main.main()
    def LB1(self, event):
        self.ZhuanHuan1.SetLabelText('->')
        self.ZhuanHuan2.SetLabelText('->')
        self.string_choose2 = []
        self.string_choose3 = []
        index = event.GetSelection()
        indexstring = self.t3.GetString(index)
        if indexstring in self.string_choose1:
            self.string_choose1.remove(indexstring)
        else:
            self.string_choose1.append(indexstring)
    def LB2(self, event):
        self.ZhuanHuan1.SetLabelText('<-')
        self.string_choose1 = []
        self.string_choose3 = []
        index = event.GetSelection()
        indexstring = self.t4.GetString(index)
        if indexstring in self.string_choose2:
            self.string_choose2.remove(indexstring)
        else:
            self.string_choose2.append(indexstring)
    def LB3(self, event):
        self.ZhuanHuan2.SetLabelText('<-')
        self.string_choose1 = []
        self.string_choose2 = []
        index = event.GetSelection()
        indexstring = self.t5.GetString(index)
        if indexstring in self.string_choose3:
            self.string_choose3.remove(indexstring)
        else:
            self.string_choose3.append(indexstring)
    def show1(self, event):
        if len(self.string_choose1)!=0:
            self.string_choose1.sort()
            for i in self.string_choose1:
                self.t4.Append(i)
                index = self.t3.FindString(i)
                self.t3.Delete(index)
        if len(self.string_choose2)!=0:
            self.string_choose2.sort()
            for i in self.string_choose2:
                self.t3.Append(i)
                index = self.t4.FindString(i)
                self.t4.Delete(index)
        self.string_choose1 = []
        self.string_choose2 = []
    def show2(self, event):
        if len(self.string_choose1)!=0:
            self.string_choose1.sort()
            for i in self.string_choose1:
                self.t5.Append(i)
                index = self.t3.FindString(i)
                self.t3.Delete(index)
        if len(self.string_choose3)!=0:
            self.string_choose3.sort()
            for i in self.string_choose3:
                self.t3.Append(i)
                index = self.t5.FindString(i)
                self.t5.Delete(index)
        self.string_choose1 = []
        self.string_choose3 = []
    def readexcel(self, path):
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        self.excel_data = []#显示的
        self.data=[]#传出去的
        for i in range(0, sheet.nrows):
            self.excel_data.append(sheet.row_values(i))
        for i in range(0, sheet.nrows):
                for j in range(0, len(self.excel_data[i])):
                    self.excel_data[i][j] = str(self.excel_data[i][j])
        for i in range(1, sheet.nrows):
            self.data.append(sheet.row_values(i))
        for i in range(0, sheet.nrows-1):
                for j in range(0, len(self.data[i])):
                    self.data[i][j] = float(self.data[i][j])
        row = len(self.excel_data)
        col = len(self.excel_data[0])
        for i in range(row):
            for j in range(col):
                self.grid.SetCellValue(i,j,self.excel_data[i][j])
        for i in range(0,len(self.excel_data[0])):
            self.t3.Append(self.excel_data[0][i])
    def readtxt(self, dir, fn):
        f = open(os.path.join(dir, fn), 'r')
        lines = f.readlines()
        row = len(lines)
        self.txt_data=[]
        self.data=[]
        for i in range(row):
            l = [str(j) for j in lines[i].split()]
            self.txt_data.append(l)
        for i in range(1,row):
            l = [float(j) for j in lines[i].split()]
            self.data.append(l)
        for i in range(row):
            for j in range(len(self.txt_data[i])):
                self.grid.SetCellValue(i, j, self.txt_data[i][j])
        for i in range(0,len(self.txt_data[0])):
            self.t3.Append(self.txt_data[0][i])
        f.close()
    def Open(self, event):
        self.t1.SetValue('')
        self.grid.ClearGrid()
        self.t3.Clear()
        self.t4.Clear()
        self.t5.Clear()
        dlg = wx.FileDialog(self, "Choose a file", "data", "", "TXT files (*.txt)|*.txt|XLSX fils(*.xlsx)|*.xlsx|"
                                                           "CSV files (*.csv)|*.csv|XLS files(*.xls)|*.xls", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            namestring = list(dlg.GetFilename())
            self.wherefile = dlg.GetDirectory()+'\\'+dlg.GetFilename()
            self.t1.SetValue(self.wherefile)
            namestring.reverse()
            if namestring[0]!='t':
                self.readexcel(self.wherefile)
            else:
                self.readtxt(dlg.GetDirectory(), dlg.GetFilename())
        dlg.Destroy()
def main(wheretogo):
    app = wx.App()
    frame = MyFrame(wheretogo)
    frame.Show()
    app.MainLoop()
    app.Destroy()
