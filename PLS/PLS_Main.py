#!/usr/bin/python
# coding=utf-8
import wx
import numpy
import pylab
import random
import PLS_Model
import numpy as np
from numpy import *
from Tkinter import *
import matplotlib.pyplot as plt
from sklearn import preprocessing

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, None, title="中医药数据分析平台", size=(600, 400))
        self.statusbar=self.CreateStatusBar()
        self.statusbar.SetStatusText(u"中医药数据分析平台")

        p=wx.Panel(self)
        p.SetBackgroundColour('white')
        nb=wx.Notebook(p)

        page1 = wx.Panel(nb)
        page2 = wx.Panel(nb)
        self.RadioButton1 = wx.RadioButton(page1, -1, "默认设置", pos=(10, 10), size=(100, 20), style=wx.RB_GROUP)
        self.RadioButton2 = wx.RadioButton(page1, -1, "自定义", pos=(120, 10,), size=(100, 20))
        self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton1, self.RadioButton1)
        self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton2, self.RadioButton2)

        #self.text = wx.StaticText(page1, -1, u'偏最小二乘回归', (160, 50), (50, -1), wx.ALIGN_CENTER)
        self.sampleList = ['10: 0', ' 9 : 1', ' 8 : 2', ' 7 : 3', ' 6 : 4']
        self.text_top01 = wx.StaticText(page1, -1, '随机划分f:', style=wx.TE_LEFT, pos=(100, 45))
        self.text_top02 = wx.StaticText(page1, -1, '主成分个数p:', style=wx.TE_LEFT, pos=(310, 45))

        self.textContents01 = wx.ComboBox(page1, pos=(200, 45), size=(55, 20), choices=self.sampleList)
        self.textContents02 = wx.TextCtrl(page1, style=wx.TE_LEFT, pos=(430, 45), size=(50, 20))
        self.textContents03 = wx.TextCtrl(page1, style=wx.TE_MULTILINE|wx.TE_READONLY, pos=(120,85), size=(340, 135))
        self.textContents04 = wx.TextCtrl(page2, style=wx.TE_MULTILINE|wx.TE_READONLY, pos=(70, 30), size=(220, 250))
        # self.test_a1 = wx.StaticText(self,-1,'显示结果:',pos=(125, 160))
        self.textContents01.SetSelection(3)
        self.textContents02.AppendText("3")
        self.textContents01.Enable(False)
        self.textContents02.Enable(False)
        #self.textContents01.Enable(False)
        #self.textContents02.Enable(False)
        #self.text.SetForegroundColour('black')

        button1 = wx.Button(page1, -1, '开始建模', pos=( 75, 240))
        button2 = wx.Button(page1, -1, ' 取  消 ', pos=(185, 240))
        button3 = wx.Button(page1, -1, ' 重  置 ', pos=(295, 240))
        button4 = wx.Button(page1, -1, '生成图形', pos=(405, 240))
        button5 = wx.Button(page2, -1, '算法简介', pos=(350,  65),size=(180, 30))
        button6 = wx.Button(page2, -1, '算法特点', pos=(350, 140),size=(180, 30))
        #button7 = wx.Button(page2, -1, '算法运用', pos=(330,  85),size=(180, 30))
        button8 = wx.Button(page2, -1, '算法缺点', pos=(350, 215),size=(180, 30))
        #button9 = wx.Button(page2, -1, '改进策略', pos=(330, 250),size=(180, 30))

        self.Bind(wx.EVT_BUTTON, self.On_Button1, button1)
        self.Bind(wx.EVT_BUTTON, self.On_Button2, button2)
        self.Bind(wx.EVT_BUTTON, self.On_Button3, button3)
        self.Bind(wx.EVT_BUTTON, self.On_Button4, button4)
        self.Bind(wx.EVT_BUTTON, self.On_Button5, button5)
        self.Bind(wx.EVT_BUTTON, self.On_Button6, button6)
        #self.Bind(wx.EVT_BUTTON, self.On_Button7, button7)
        self.Bind(wx.EVT_BUTTON, self.On_Button8, button8)
        #self.Bind(wx.EVT_BUTTON, self.On_Button9, button9)

        font  = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)
        font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
        #font2 = wx.Font(24, wx.MODERN, wx.NORMAL, wx.BOLD)
        self.text_top01.SetFont(font)
        self.text_top02.SetFont(font)
        # self.text.SetFont(font2)
        button1.SetFont(font)
        button2.SetFont(font)
        button3.SetFont(font)
        button4.SetFont(font)
        button5.SetFont(font)
        button6.SetFont(font)
        #button7.SetFont(font)
        button8.SetFont(font)
        #button9.SetFont(font)

        nb.AddPage(page1, "参数设置")
        nb.AddPage(page2, "其它信息")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

#开始建模
    def On_Button1(self, event):
        self.textContents03.Clear()
        if self.textContents01.GetValue() <= ' ':
            wx.MessageBox("请输入完整的信息!", "警告", wx.OK | wx.ICON_INFORMATION)
            self.textContents01.SetValue('')
            self.textContents02.Clear()
            return
        elif self.textContents02.GetValue() <= ' ':
            wx.MessageBox("请输入完整的信息!", "警告", wx.OK | wx.ICON_INFORMATION)
            self.textContents01.SetValue('')
            self.textContents02.Clear()
            return

        else:
            global xishu, m, xish, SSE, SST, SSR, RR1, RMSE, y0, y_predict, train_y
            x0, y0 = PLS_Model.loadDataSet01('data\TCMdata.txt')
            f = self.textContents01.GetValue()
            p = self.textContents02.GetValue()

            def is_float(str):
                if str.count('.') == 1:
                    left = str.split('.')[0]
                    right = str.split('.')[1]
                    lright = ''
                    if str.count('-') == 1 and str[0] == '-':
                        lright = left.split('-')[1]
                    elif str.count('-') == 0:
                        lright = left
                    else:
                        return 0
                    if right.isdigit() and lright.isdigit():
                        return 1

            if p.isdigit() == True:
                pass
            else:
                wx.MessageBox("请按照规定格式输入p值，请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
                self.textContents02.Clear()
                return

            if is_float(str(p)) == 1:
                wx.MessageBox("p的值为整数，请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
                self.textContents02.Clear()
                return

            p = float(p)
            if p <= 0:
                wx.MessageBox("p的值过小，请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
                self.textContents02.Clear()
                return 0

            if f == '10: 0':
                q = 1
            elif f == ' 9 : 1':
                q = 0.9
            elif f == ' 8 : 2':
                q = 0.8
            elif f == ' 7 : 3':
                q = 0.7
            elif f == ' 6 : 4':
                q = 0.6

            if q==1:
                e0, f0 = PLS_Model.stardantDataSet(x0, y0)
                h = 0
                e0 = mat(e0)
                f0 = mat(f0)
                m = shape(x0)[1]
                ny = shape(y0)[1]
                my = shape(x0)[0]
                chg = mat(eye((m)))
                t = mat(zeros((my, m)))
                w = mat(zeros((m, m))).T
                ss= mat(zeros((m, 1))).T
                alpha= mat(zeros((m, m)))
                press= mat(zeros((1, m)))
                Q_h2 = mat(zeros((1, m)))
                beta = mat(zeros((1, m))).T
                w_star = mat(zeros((m, m))).T
                press_i = mat(zeros((1, my)))

                for i in range(1,m+1):
                    matrix = e0.T * f0 * (f0.T * e0)
                    val, vec = linalg.eig(matrix)
                    sort_val = argsort(val)
                    w[:, i - 1] = vec[:, sort_val[:-2:-1]]
                    w_star[:, i - 1] = chg * w[:, i - 1]
                    t[:, i - 1] = e0 * w[:, i - 1]
                    alpha[:,i- 1]= (e0.T* t[:,i- 1])/ (t[:,i- 1].T* t[:,i- 1])
                    chg = chg * mat(eye((m))- w[:, i - 1] * alpha[:, i - 1].T)
                    e = e0 - t[:, i - 1] * alpha[:, i - 1].T
                    e0 = e
                    beta[i- 1, :]= (t[:,i- 1].T* f0)/ (t[:,i- 1].T* t[:,i- 1])
                    cancha = f0 - t * beta
                    ss[:,i- 1]= sum(sum(power(cancha,2),0),1)

                    for j in range(1, my + 1):
                        if i == 1:
                            t1 = t[:, i - 1]
                        else:
                            t1 = t[:, 0:i]
                        f1 = f0
                        she_t = t1[j - 1, :]
                        she_f = f1[j - 1, :]
                        t1 = list(t1)
                        f1 = list(f1)
                        del t1[j - 1]
                        del f1[j - 1]
                        t1 = array(t1)
                        f1 = array(f1)

                        if i == 1:
                            t1 = mat(t1).T
                            f1 = mat(f1).T
                        else:
                            t1 = mat(t1)
                            f1 = mat(f1).T
                        beta1 = linalg.inv(t1.T* t1)* (t1.T* f1)
                        cancha= she_f- she_t* beta1
                        press_i[:,j- 1]= sum(power(cancha,2))

                    press[:, i - 1] = sum(press_i)
                    if i > 1:
                        Q_h2[:,i- 1]= 1- press[:,i- 1]/ ss[:,i- 2]
                    else:
                        Q_h2[:, 0] = 1
                    if Q_h2[:, i - 1] < 0.0975:
                        h = i
                    if h == p:
                        break

                mean_x, mean_y, std_x, std_y = PLS_Model.data_Mean_Std(x0, y0)
                n = shape(y0)[1]
                row = shape(x0)[0]
                xishu = w_star * beta
                train_y = y0
                ch0, xish = PLS_Model.Calxishu(xishu, mean_x, mean_y, std_x, std_y)

                y_predict = x0 * xish + tile(ch0[0, :], (row, 1))
                y_mean = tile(mean_y, (row, 1))
                SSE = sum(sum(power((y0        - y_predict), 2), 0))
                SST = sum(sum(power((y0        - y_mean   ), 2), 0))
                SSR = sum(sum(power((y_predict - y_mean   ), 2), 0))
                RR = SSR / SST
                RMSE = sqrt(SSE / row)

            else:
                train_x, train_y = PLS_Model.splitDataSet(x0, y0, q)
                e0, f0 = PLS_Model.stardantDataSet(train_x, train_y)
                h = 0
                e0= mat(e0)
                f0= mat(f0)
                m = shape(train_x)[1]
                ny= shape(train_y)[1]
                my= shape(train_x)[0]
                chg = mat(eye((m)))
                t = mat(zeros((my, m)))
                w = mat(zeros((m, m))).T
                ss= mat(zeros((m, 1))).T
                alpha= mat(zeros((m, m)))
                press= mat(zeros((1, m)))
                Q_h2 = mat(zeros((1, m)))
                beta  = mat(zeros((1, m))).T
                w_star= mat(zeros((m, m))).T
                press_i = mat(zeros((1, my)))

                for i in range(1, m + 1):
                    matrix = e0.T * f0 * (f0.T * e0)
                    val, vec = linalg.eig(matrix)
                    sort_val = argsort(val)
                    w[:, i - 1] = vec[:, sort_val[:-2:-1]]
                    w_star[:, i - 1] = chg * w[:, i - 1]
                    t[:, i - 1] = e0 * w[:, i - 1]
                    alpha[:,i- 1]= (e0.T* t[:,i- 1])/ (t[:,i- 1].T* t[:,i- 1])
                    chg = chg* mat(eye((m))- w[:,i- 1]* alpha[:,i- 1].T)
                    e = e0 - t[:, i - 1] * alpha[:, i - 1].T
                    e0 = e
                    beta[i- 1, :]= (t[:,i- 1].T* f0)/ (t[:,i- 1].T* t[:,i- 1])
                    cancha = f0 - t * beta
                    ss[:, i - 1] = sum(sum(power(cancha, 2), 0), 1)

                    for j in range(1, my + 1):
                        if i == 1:
                            t1 = t[:, i - 1]
                        else:
                            t1 = t[:, 0:i]
                        f1 = f0
                        she_t = t1[j - 1, :]
                        she_f = f1[j - 1, :]
                        t1 = list(t1)
                        f1 = list(f1)
                        del t1[j - 1]
                        del f1[j - 1]
                        t1 = array(t1)
                        f1 = array(f1)

                        if i == 1:
                            t1 = mat(t1).T
                            f1 = mat(f1).T
                        else:
                            t1 = mat(t1)
                            f1 = mat(f1).T
                        #beta1 = linalg.inv(t1.T * t1) * (t1.T * f1)
                        beta1 = (t1.T * t1) * (t1.T * f1)
                        cancha = she_f - she_t * beta1
                        press_i[:, j - 1] = sum(power(cancha, 2))
                    press[:, i - 1] = sum(press_i)

                    if i > 1:
                        Q_h2[:, i - 1] = 1 - press[:, i - 1] / ss[:, i - 2]
                    else:
                        Q_h2[:, 0] = 1
                    if Q_h2[:, i - 1] < 0.0975:
                        h = i
                    if h == p:
                        break

                mean_x, mean_y, std_x, std_y = PLS_Model.data_Mean_Std(train_x, train_y)
                n = shape(train_y)[1]
                row = shape(train_x)[0]
                xishu = w_star * beta
                ch0, xish = PLS_Model.Calxishu(xishu, mean_x, mean_y, std_x, std_y)

                y_predict = train_x * xish + tile(ch0[0, :], (row, 1))
                y_mean = tile(mean_y, (row, 1))
                SSE = sum(sum(power((train_y   - y_predict), 2), 0))
                SST = sum(sum(power((train_y   - y_mean   ), 2), 0))
                SSR = sum(sum(power((y_predict - y_mean   ), 2), 0))
                RR = SSR / SST
                RMSE = sqrt(SSE / row)

            if p>m:
                wx.MessageBox("p的值过大，请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
                self.textContents02.Clear()
                return 0

            self.textContents03.AppendText('==============显示结果===============' + '\n' + '\n')
            self.textContents03.AppendText('1.残差平方和SSE:' + '  ' + str(SSE) + '\n')
            self.textContents03.AppendText('2.回归平方和SSR:' + '  ' + str(SSR) + '\n')
            self.textContents03.AppendText('3.离差平方和SST:' + '  ' + str(SST) + '\n')
            self.textContents03.AppendText('4.可决系数R-Square:' + '  ' + str(RR) + '\n')
            self.textContents03.AppendText('5.均方根误差RMSE: '+ '  '  + str(RMSE) + '\n')
            self.textContents03.AppendText('6.系数xishu:'+ '  '  + str(ch0 ) + '\n')
            self.textContents03.AppendText(''+ str(xish) + '\n' + '\n')
            self.textContents03.AppendText('==============显示结果===============')

#取消
    def On_Button2(self, event):
        self.Close(True)

#重置
    def On_Button3(self, event):
        self.textContents01.SetValue('')
        self.textContents01.SetSelection(3)
        self.textContents02.Clear()
        self.textContents02.AppendText("3")
        self.textContents03.Clear()

#生成图形
    def On_Button4(self, event):
        if self.textContents03.GetValue() <= ' ':
            wx.MessageBox("请先点击'开始建模'按钮!", "警告", wx.OK | wx.ICON_INFORMATION)
            return

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title('Partial Least - Squares Regression')
        ax.plot(y_predict, 'r:', markerfacecolor='blue', marker='o')
        plt.annotate('y_predict', xy=(6, 0.090), xytext=(4, 0.10),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        ax.plot(y0, markerfacecolor='red', marker='h')
        plt.annotate('y0', xy=(7.2, 0.058), xytext=(8, 0.05),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.grid(True)
        plt.show()


#算法简介
    def On_Button5(self, event):
        self.textContents04.Clear()
        self.textContents04.AppendText('偏最小二乘回归方法简介：\n  \n'
                                       '    偏最小二乘回归方法是一种新型的多元统计数据分析方法，它主要'
                                       '研究的是多因变量对多自变量的回归建模，用以解决医药化学样本分析'
                                       '中存在的变量多重相关，以及解释变量多于样本点等实际问题。\n \n'
                                       '    偏最小二乘回归是一种集主成分分析,典型相关分析和多元线性回归'
                                       '分析3种分析方法的优点于一身的方法。它与主成分分析法都试图提取出'
                                       '反映数据变异的最大信息，但主成分分析法只考虑一个自变量矩阵，而偏'
                                       '最小二乘法还有一个‘响应’矩阵，因此具有预测功能。\n \n'
                                       '    由于偏最小二乘回归方法能解决许多以往用普通多元回归无法解决的'
                                       '问题，因而得到了有关研究人员的重视，在线性与非线性的偏最小二乘回'
                                       '归的理论及方法上发展迅速。')

# 算法特点
    def On_Button6(self, event):
        self.textContents04.Clear()
        self.textContents04.AppendText('偏最小二乘回归方法的特点：\n  \n'
                                       '(1)允许在样本点个数小于变量个数的条件下进行建模；\n \n'
                                       '(2)偏最小二乘回归在最终模型中将包含原有的所有自变量；\n \n'
                                       '(3)偏最小二乘回归可以实现多种数据分析方法的综合应用；\n \n'
                                       '(4)能够在自变量存在严重多重相关性的条件下进行回归建模；\n \n'
                                       '(5)偏最小二乘回归模型易于辨识系统信息与噪音，而且其自变量'
                                           '的回归系数也将更容易解释；\n \n'
                                       '(6)偏最小二乘回归方法与其他的建模方法相比，具有技术简单、'
                                           '预测精度高，易于定性解释的优点。')

# 算法缺点
    def On_Button8(self, event):
        self.textContents04.Clear()
        self.textContents04.AppendText('偏最小二乘回归方法的缺点：\n  \n'
                                       '(1)偏最小二乘回归方法是一种线性回归方法，因而无法对医学上'
                                          '那些非线性的数据进行回归分析建模；\n \n'
                                       '(2)偏最小二乘回归方法内部无特征选择操作，故无法实现对医学'
                                          '上高维数据的降维操作。')

#默认设置
    def On_RadioButton1(self, event):
        self.textContents02.Clear()
        self.textContents03.Clear()
        self.textContents01.SetValue('')
        self.textContents01.SetSelection(3)
        self.textContents02.AppendText('3')
        self.textContents01.Enable(False)
        self.textContents02.Enable(False)

#自定义
    def On_RadioButton2(self, event):
        self.textContents02.Clear()
        self.textContents03.Clear()
        self.textContents01.SetValue('')
        self.textContents01.SetSelection(3)
        self.textContents02.AppendText('3')
        self.textContents01.Enable(True)
        self.textContents02.Enable(True)



def main():
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    frame.Center()
    app.MainLoop()