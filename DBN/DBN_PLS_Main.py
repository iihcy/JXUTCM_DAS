# coding:utf-8
# !/usr/bin/env python
# include <wx/notebook.h>
import wx
import DBN_PLS_Model


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="DBN_PLS WINDOW", size=(600, 400))
        p = wx.Panel(self)
        self.nb = wx.Notebook(p)
        p.SetBackgroundColour('#3299CC')

        #第一页（参数设置）
        self.page1 =wx.Panel(self.nb)
        self.rb1 = wx.RadioButton(self.page1, 1, label='默认', pos=(200, 25))
        self.rb2 = wx.RadioButton(self.page1, 2, label='自定义', pos=(300, 25))
        self.Label1 = wx.StaticText(self.page1, -1, "预训练次数：", pos=(120, 70))
        self.Text1 = wx.TextCtrl(self.page1, -1, pos=(220, 65), size=(205, 20))
        self.Label2 = wx.StaticText(self.page1, -1, "预训练学习率:", pos=(120, 110))
        self.Text2 = wx.TextCtrl(self.page1, -1, pos=(220, 105), size=(205, 20))
        self.Label3 = wx.StaticText(self.page1, -1, "抽样步数:", pos=(120, 150))
        self.Text3 = wx.TextCtrl(self.page1, -1, pos=(220, 145), size=(205, 20))
        self.Label4 = wx.StaticText(self.page1, -1, "批处理大小：", pos=(120, 190))
        self.Text4 = wx.TextCtrl(self.page1, -1, pos=(220, 185), size=(205, 20))
        self.Label5 = wx.StaticText(self.page1, -1, "DBN层数：", pos=(120,230))
        self.Text5 =wx.TextCtrl( self.page1, -1, pos=(220,225), size=(205,20))
        self.Button1 = wx.Button(self.page1, -1, label='开始建模', pos=(120, 270))
        self.Button2 = wx.Button(self.page1, -1, label='重置', pos=(230, 270))
        self.Button3 = wx.Button(self.page1, -1, label='取消', pos=(340, 270))
        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.moren)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.zdy)
        self.Button1.Bind(wx.EVT_BUTTON, self.Onclicked1)
        self.Button2.Bind(wx.EVT_BUTTON, self.Onclicked2)
        self.Button3.Bind(wx.EVT_BUTTON, self.Onclicked3)
        self.Bind(wx.EVT_CLOSE, self.Onclicked4)
        self.rb1.SetValue(True)
        self.Text1.SetValue('10')
        self.Text2.SetValue('0.1')
        self.Text3.SetValue('1')
        self.Text4.SetValue('10')
        self.Text5.SetValue('10,10,8,5,5')
        self.Text1.Enable(False)
        self.Text2.Enable(False)
        self.Text3.Enable(False)
        self.Text4.Enable(False)
        self.Text5.Enable(False)

        #第二页（模型结果）
        self.page2 = wx.Panel(self.nb)
        self.button = wx.Button(self.page2, wx.NewId(), "模型结果", (250, 270), (100, 40))
        self.sendtext = wx.TextCtrl(self.page2, wx.NewId(), '',(100, 50), (400, 200), wx.TE_LEFT | wx.TE_MULTILINE)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)


        #第三页（其他信息）
        self.page3 = wx.Panel(self.nb)
        self.textContents002 = wx.StaticText(self.page3, -1, 'PLS: ', (50, 10))
        font1 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.textContents002.SetFont(font1)
        self.extContents003 = wx.StaticText(self.page3, -1,
                                        '(1)集成主成分分析、典型相关性分析和多元线性回归分析方法的特点\n  \n(2)其内部采用的交叉核验方法会导致主成分急剧减少，从而降低回归\n  \n方程的精度，而中医药数据对主成分的选取尤为敏感。 ',
                                        (75, 45))
        font2 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.extContents003.SetFont(font2)
        self.textContents004 = wx.StaticText(self.page3, -1, 'DBN-PLS: ', (50, 135))
        font3 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.textContents004.SetFont(font3)
        self.textContents005 = wx.StaticText(self.page3, -1,
                                        '   DBN-PLS方法是利用DBN取代PLS中主成分提取部分，采用DBN抽取的\n  \n原始数据的上层特征作为主成分，然后利用偏最小二乘外模型进行回归\n  \n建模，最后还原成原始变量的回归方程，通过测试数据的验证反过来调\n  \n整深度学习模型的参数以及隐层的层数，最终达到提高回归方程的精度\n  \n的目的。',
            (65, 165))
        font4 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.textContents005.SetFont(font4)

        self.nb.InsertPage(0, self.page1, "参数设置", False)
        self.nb.InsertPage(1, self.page2, "模型结果", False)
        self.nb.InsertPage(2, self.page3, "其它信息", False)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)

        p.SetSizer(sizer)

    #第一页事件
    #开始建模按钮事件
    def Onclicked1(self, event):
        if self.Text1.GetValue() == '' or self.Text2.GetValue() == '' or self.Text3.GetValue() == '':
            wx.MessageBox("参数值不能为空", "警告", wx.OK | wx.ICON_INFORMATION)
        else:
            #跳转事件
            self.nb.SetSelection(1)
            #进度条
            progressMax = 2
            dialog = wx.ProgressDialog("正在运行", "Time remaining", progressMax,
                                       style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
            keepGoing = True
            count = 0
            while keepGoing and count < progressMax:
                count = count + 1
                wx.Sleep(1)
                keepGoing = dialog.Update(count)
                # 传参
                a = int(self.Text1.GetValue())
                b = float(self.Text2.GetValue())
                c = int(self.Text3.GetValue())
                d = int(self.Text4.GetValue())
                self.SSE, self.SSR, self.RR, self.RMSE, self.ch0, self.xish = DBN_PLS_Model.canshu(a, b, c, d)
                dialog.Destroy()

    #重置按钮事件
    def Onclicked2(self, event):
        self.Text1.SetValue('')
        self.Text2.SetValue('')
        self.Text3.SetValue('')
        self.Text4.SetValue('')
        self.Text5.SetValue('')

    #取消按钮事件
    def Onclicked3(self, event):
        self.Close(True)

    def Onclicked4(self, event):
        self.Destroy()

    #默认RadioButton事件
    def moren(self, event):
        self.Text1.SetValue('10')
        self.Text2.SetValue('0.1')
        self.Text3.SetValue('1')
        self.Text4.SetValue('10')
        self.Text5.SetValue('10,10,8,5,5')
        self.Text1.Enable(False)
        self.Text2.Enable(False)
        self.Text3.Enable(False)
        self.Text4.Enable(False)
        self.Text5.Enable(False)

    #自定义RadioButton事件
    def zdy(self, e):
        self.Text1.Enable(True)
        self.Text2.Enable(True)
        self.Text3.Enable(True)
        self.Text4.Enable(True)
        self.Text5.Enable(True)
    # 第一页事件结束

    #第二页事件
    #建模结果按钮事件
    def OnClick(self, event):

        RR = str(self.RR)
        RMSE = str(self.RMSE)
        SSE = str(self.SSE)
        ch0 = str(self.ch0)
        xish = str(self.xish)
        self.sendtext.Clear()
        self.sendtext.AppendText(
            '====结果摘要===' + '\n' + '1.可决系数:RR' + '\n' + RR + '\n' + '**********************' + '\n' + '2.均方根误差RMSE:' + '\n' + RMSE + '\n'
            + '**********************' + '\n' + '3.残差平方和SSE:' + '\n' + SSE + '\n' + '**********************' + '\n' + '4.系数:' + '\n' + ch0 + '\n' + '**********************' +
            '\n' + '5.回归系数:' + '\n' + xish + '\n' + '**********************' + '\n')


def main():
    app = wx.App()
    frame = MainFrame()
    frame.SetMaxSize((600, 400))
    frame.SetMinSize((600, 400))
    frame.Show()
    app.MainLoop()
