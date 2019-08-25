# coding:utf-8
#!/usr/bin/env python
# include <wx/notebook.h>

from numpy import *
import pandas as pd
import wx
import Lasso_PLS_Model
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import numpy as np



class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('white')
        RadioButton1 = wx.RadioButton(self, -1, "默认设置", pos=(100, 20), size=(70, 20),style=wx.RB_GROUP)
        RadioButton2 = wx.RadioButton(self, -1, "自定义", pos=(210, 20,), size=(70, 20))
        self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton1, RadioButton1)
        self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton2, RadioButton2)

        sampleList = ['10:0', '9:1', '8:2', '7:3', '6:4']

        self.text_top00=wx.StaticText(self, -1, "样本随机划分:", (100, 65))
        self.Combo = wx.ComboBox(self, -1, pos=(180, 60), size=(60, 30), choices=sampleList)


        self.text_top01 = wx.StaticText(self, -1, '成分个数:', style=wx.TE_LEFT, pos=(100, 105))
        self.textContents01 = wx.TextCtrl(self, style=wx.TE_LEFT, pos=(180, 100), size=(300, 30))
        self.text_top02 = wx.StaticText(self, -1, 'λ:', style=wx.TE_LEFT, pos=(100, 140))
        self.textContents02 = wx.TextCtrl(self, style=wx.TE_LEFT, pos=(180, 135), size=(300, 30))
        self.text_top03 = wx.StaticText(self, -1, '预值:', style=wx.TE_LEFT, pos=(100, 175))
        self.textContents03 = wx.TextCtrl(self, style=wx.TE_LEFT, pos=(180, 170), size=(300, 30))
        # font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        # self.text_top01.SetFont(font)
        # self.text_top02.SetFont(font)
        # self.text_top03.SetFont(font)
        # self.text_top00.SetFont(font)



        button1 = wx.Button(self, -1, '开始建模', pos=(100, 240))
        self.Bind(wx.EVT_BUTTON, self.On_Button1, button1)
        button2 = wx.Button(self, -1, '重置', pos=(245, 240))
        self.Bind(wx.EVT_BUTTON, self.On_Button2, button2)
        button3 = wx.Button(self, -1, '取消', pos=(390, 240))
        self.Bind(wx.EVT_BUTTON, self.On_Button3, button3)
        h=3
        lambd_k=9
        th_k = 0.2

        h = str(h)
        lambd_k = str(lambd_k)
        th_k = str(th_k)
        self.textContents01.AppendText(h)
        self.textContents02.AppendText(lambd_k)
        self.textContents03.AppendText(th_k)
        self.Combo.SetValue(sampleList[0])
        self.textContents01.Enable(False)
        self.textContents02.Enable(False)
        self.textContents03.Enable(False)
        self.Combo.Enable(False)


#开始建模
    def On_Button1(self, event):
        global m,xish,SSE, SST, SSR, RR1, RMSE,y_predict,y0,xish1

        c=7.0;d=0.1
        if self.textContents01.GetValue() <= '0': wx.MessageBox("成分个数不能为空或为0", "警告", wx.OK | wx.ICON_INFORMATION)
        if float(self.textContents02.GetValue()) <= c : wx.MessageBox("λ值要大于7", "警告", wx.OK | wx.ICON_INFORMATION)
        if float(self.textContents03.GetValue()) <= d: wx.MessageBox("预值要大于0.1", "警告", wx.OK | wx.ICON_INFORMATION)

        x0, y0 = Lasso_PLS_Model.loadDataSet01('data\TCMdata.txt')  # 单因变量与多因变量
        # 随机划分数据集- 7:3
        f = self.Combo.GetValue()
        if f=="10:0":
            k=1
        elif f=="9:1":
            k=0.9
        elif f=="8:2":
            k=0.8
        elif f=="7:3":
            k=0.7
        else:
            k=0.6
        train_x, train_y, test_x, test_y = Lasso_PLS_Model.splitDataSet(x0, y0,k)
        # 标准化
        e0, f0 = Lasso_PLS_Model.stardantDataSet(train_x, train_y)
        mean_x, mean_y, std_x, std_y = Lasso_PLS_Model.data_Mean_Std(x0, y0)
        r = corrcoef(x0)
        m = shape(x0)[1]
        n = shape(y0)[1]  # 自变量和因变量个数
        row = shape(x0)[0]

        h1 =float( self.textContents01.GetValue())
        lambd_k1 = float(self.textContents02.GetValue())
        th_k1 =float(self.textContents03.GetValue())

        h1=float(h1)
        lambd_k1=float(lambd_k1)
        th_k1=float(th_k1)

        h, w_star, t, beta = Lasso_PLS_Model.PLS(x0, y0, h1)

        xishu = w_star * beta
        # 反标准化

        ch0, xish1 = Lasso_PLS_Model.Calxishu(xishu, mean_x, mean_y, std_x, std_y)

        # Lasso处理--不显著变量的系数设置为0
        ntest = 20
        #th_k = 0.2  # th_k取值得大于0.1，建议精度至4个小数点（最佳取值th_k = 0.2）--默认值0.2
        #lambd_k = 9  # lambd_k得大于7，最佳取值lambd_k=9(默认值)

        ws = Lasso_PLS_Model.lasso_traj(e0, f0, ntest, th_k1, lambd_k1)
        dataframe = pd.DataFrame(ws)
        dataframe.to_csv(u'回归系数迭代.csv')
        xish = Lasso_PLS_Model.PLS_xish(e0, f0, ntest, th_k1,lambd_k1)
        # 求可决系数和均方根误差
        y_predict= x0 * xish + tile(ch0[0, :], (row, 1))

        y_mean = tile(mean_y, (row, 1))
        SSE = sum(sum(power((y0 -y_predict), 2), 0))
        SST = sum(sum(power((y0 - y_mean), 2), 0))
        SSR = sum(sum(power(( y_predict- y_mean), 2), 0))

        RR1 = SSR / SST
        RMSE = sqrt(SSE / row)
        Lasso_PLS_Model.parameter_Errors(th_k1, lambd_k1)
        nb.SetSelection(1)        #跳转第二个选项卡
#重置
    def On_Button2(self, event):
        self.textContents01.Clear()
        self.textContents02.Clear()
        self.textContents03.Clear()
        self.Combo.SetValue(' ')    #比例清零

        self.textContents01.Enable(True)  #设置不可改
        self.textContents02.Enable(True)
        self.textContents03.Enable(True)
        self.Combo.Enable(True)
#取消
    def On_Button3(self, event):
        self.Close()
#默认设置
    def On_RadioButton1(self, event):
        h = 3
        lambd_k = 9
        th_k = 0.2
        sampleList = ['10:0', '9:1', '8:2', '7:3', '6:4']
        h = str(h)
        lambd_k = str(lambd_k)
        th_k = str(th_k)
        self.textContents01.Clear()
        self.textContents02.Clear()
        self.textContents03.Clear()
        self.textContents01.AppendText(h)
        self.textContents02.AppendText(lambd_k)
        self.textContents03.AppendText(th_k)
        self.Combo.SetValue(sampleList[0])
        self.textContents01.Enable(False)
        self.textContents02.Enable(False)
        self.textContents03.Enable(False)
        self.Combo.Enable(False)
#自定义
    def On_RadioButton2(self, event):
        self.textContents01.Enable(True)
        self.textContents02.Enable(True)
        self.textContents03.Enable(True)
        self.Combo.Enable(True)



class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('white')
        #self.SetBackgroundColour('#3299CC')
        self.multiLabel = wx.StaticText(self, -1, "选择后的特征", pos=(250, 10))
        self.richText = wx.TextCtrl(self, -1, size=(400, 30), pos=(90, 30), style=wx.TE_MULTILINE|wx.TE_CENTER)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.richText.SetFont(font)
        #plsLabel = wx.StaticText(self, -1, "PLS", pos=(195, 80))
        self.plsText = wx.TextCtrl(self, -1,size=(120, 220), pos=(90, 70), style=wx.HSCROLL |wx.TE_MULTILINE)

        #LassoLabel = wx.StaticText(self, -1, "Lasso\n—pls", pos=(350, 70))
        self.LassoText = wx.TextCtrl(self, -1,size=(120, 220), pos=(370, 70), style=wx.HSCROLL |wx.TE_MULTILINE)

        plsButton = wx.Button(self, label='PLS系数', pos=(245, 110),size=(90,40))
        LassoButton = wx.Button(self, label='特征选择系数', pos=(245, 160),size=(90,40))
        jieButton = wx.Button(self, label='模型结果', pos=(245, 210), size=(90, 40))

        self.Bind(wx.EVT_BUTTON,self.On_plsButton, plsButton)
        self.Bind(wx.EVT_BUTTON, self.On_LassoButton, LassoButton)
        self.Bind(wx.EVT_BUTTON, self.On_jieButton, jieButton)


    def On_plsButton(self,event):
        global xish1,m
        xishu1=xish1
        xishu1 = xishu1.tolist()

        self.plsText.Clear()
        self.plsText.AppendText('===PLS系数===')
        self.plsText.AppendText('\n')
        for i in range(m):
            xishu1[i] = str(xishu1[i])
            xishu1[i] = xishu1[i].replace("[", "")
            xishu1[i] = xishu1[i].replace("]", "")
            i1=str(i+1)
            self.plsText.AppendText('x'+i1+': '+xishu1[i])
            self.plsText.AppendText('\n')

    def On_LassoButton(self,event):
        global xish,m
        xish1=xish
        xish1 = xish1.tolist()
        self.LassoText.Clear()
        self.richText.Clear()
        self.LassoText.AppendText('特征选择后系数')
        self.LassoText.AppendText('\n')
        for i in range(m):
            xish1[i] = str(xish1[i])
            xish1[i] = xish1[i].replace("[", "")
            xish1[i] = xish1[i].replace("]", "")
            i2=str(i+1)
            self.LassoText.AppendText('x'+i2+': '+xish1[i])
            self.LassoText.AppendText('\n')
            xish1[i]=float(xish1[i])
            if xish1[i] != 0:
                self.richText.AppendText('x'+i2+'   ')
                #self.richText.AppendText('，')
    def On_jieButton(self,event):
        nb.SetSelection(2)

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.textContents001 = wx.TextCtrl(self, style=wx.TE_LEFT | wx.TE_MULTILINE, pos=(440, 0), size=(140, 264))
        modelResult = wx.Button(self, label='数据结果', pos=(460, 270))
        imageResult = wx.Button(self, label='模型图', pos=(160, 270))

        self.Bind(wx.EVT_BUTTON, self.On_modelResult, modelResult)
        self.Bind(wx.EVT_BUTTON, self.On_imageResult, imageResult)

        y0=Lasso_PLS_Model.canshu1()

        self.figure = plt.figure(figsize=(5.5, 3.3),facecolor='white')
        self.ax = self.figure.add_subplot(111)

        self.ax.plot(y0, markerfacecolor='red', marker='h')
        plt.annotate('y_actual', xy=(7.1, 0.055), xytext=(7.3, 0.025),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        self.ax.set_title('illustraton of model')
        self.canvas = FigureCanvas(self, 8, self.figure)


        plt.grid(True)
        self.Fit()




    def On_modelResult(self,event):
        global SSE, SST, SSR, RR1, RMSE
        SSE = str(SSE);SST = str(SST);SSR = str(SSR);RR1 = str(RR1);RMSE = str(RMSE)
        SSE2, SST2, SSR2, RR2, RMSE2=Lasso_PLS_Model.canshu2()
        SSE2 = str(SSE2);SST2 = str(SST2);SSR2 = str(SSR2);RR2 = str(RR2);RMSE2 = str(RMSE2)
        self.textContents001.Clear()
        self.textContents001.AppendText(
            '====结果摘要===' + '\n' + 'PLS数据结果' + '**********************' + '\n' + '残差平方和SSE:' + '\n' + SSE2 + '\n' + '**********************' + '\n' +
            '实际误差平方和SST:' + '\n' + SST2 + '\n' + '**********************' + '\n' + '回归平方和SSR:' + '\n' + SSR2 + '\n' + '**********************'
            + '\n' + 'R的平方RR:' + '\n' + RR2 + '\n' + '**********************' + '\n' + '均方根误差RMSE:' + '\n' + RMSE2 + '\n' + '**********************'

            + '选择后数据结果' + '**********************' + '\n' + '残差平方和SSE:' + '\n' + SSE + '\n' + '**********************' + '\n' +
            '实际误差平方和SST:' + '\n' + SST + '\n' + '**********************' + '\n' + '回归平方和SSR:' + '\n' + SSR + '\n' + '**********************'
            + '\n' + 'R的平方RR:' + '\n' + RR1 + '\n' + '**********************' + '\n' + '均方根误差RMSE:' + '\n' + RMSE + '\n' + '**********************')


    def On_imageResult(self,event):
        y_PLS_predict=Lasso_PLS_Model.canshu3()
        figure = plt.figure(figsize=(5.5,3.3),facecolor='white')
        ax = figure.add_subplot(111)
        #t = arange(0.0, 3.0, 0.01)
        ax.plot(y_predict, 'r:', markerfacecolor='blue', marker='o')
        plt.annotate('y_predict(Lasso_PLS)', xy=(6, 0.090), xytext=(4, 0.15),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        #s = sin(2 * pi * t)
        ax.plot(y0, markerfacecolor='red', marker='h')
        plt.annotate('y_actual', xy=(7.1, 0.055), xytext=(7.3, 0.025),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        # plt.annotate('actual_y0', xy=(7.2, 0.058), xytext=(8, 0.05),
        #              arrowprops=dict(facecolor='black', shrink=0.05))
        #self.axes.plot(t, s)
        ax.plot(y_PLS_predict, markerfacecolor='yellow', marker='h')
        ax.set_title('illustraton of model')

        plt.grid(True)
        self.Fit()
        self.canvas = FigureCanvas(self, 8, figure)

class PageFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        textContents002 = wx.StaticText(self, -1, 'PLS优点: ', (70, 10))
        font1 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        textContents002.SetFont(font1)
        textContents003 = wx.StaticText(self, -1,
                                        '(1)能够在自变量存在严重多重相关性的条件下进行回归建模\n  \n(2)允许在样本点个数小于变量个数的条件下进行建模\n  \n(3)偏最小二乘回归在最终模型中将包含原有的所有自变量 ',
                                        (90, 40))
        font2 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        textContents003.SetFont(font2)
        textContents004 = wx.StaticText(self, -1, 'Lasso: ', (70, 130))
        font3 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        textContents004.SetFont(font3)
        textContents005 = wx.StaticText(self, -1,
                                        ' Lasso方法是一种压缩估计,它通过构造一个惩罚函数得到\n \n 一个较为精炼的模型，使得它压缩一些系数，同时设定一\n \n 些系数为零,进而达到特征选择的目的',
                                        (90, 160))
        font4 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        textContents005.SetFont(font4)




class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Lasso_PLS",size=(600,400),style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))
        m,n,row=Lasso_PLS_Model.canshu()
        g = str(row)
        m = str(m)
        n = str(n)

        self.statusbar = self.CreateStatusBar()

        self.statusbar.SetStatusText('Lasso-PLS中医药数据分析      '+'X数据行和列:'+g+'*'+m+'      '+'Y数据行和列:'+g+'*'+n)
        setImg=wx.Image('Lasso_PLS\sc.jpg',wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        setIcon=wx.Icon(setImg)
        self.SetIcon(setIcon)
        p = wx.Panel(self)
        global nb
        nb = wx.Notebook(p)
        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)
        page4=PageFour(nb)

        nb.AddPage(page1, "参数设置")
        nb.AddPage(page2, "特征选择")
        nb.AddPage(page3, "模型结果")
        nb.AddPage(page4,'其它信息')

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


def main():
    app = wx.App()
    frame= MainFrame()
    frame.Show()
    frame.Center()
    frame.SetMaxSize((600, 400))
    frame.SetMinSize((600, 400))
    app.MainLoop()