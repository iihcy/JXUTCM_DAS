#!/usr/bin/python
# coding=utf-8
import pylab
import wx
from Tkinter import *
import coordinate
import Coordinate1
import KNN_Model
k = str(3)
num=str(0.263499)
A=str(42330)
B=str(11.492186)
AN=0
#第一选项卡
class PageOne(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.RadioButton1 = wx.RadioButton(self, -1, "默认设置", pos=(10, 5), size=(100, 20),style = wx.RB_GROUP)
        self.RadioButton2 = wx.RadioButton(self, -1, "自定义", pos=(110, 5), size=(100, 20))
        self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton1, self.RadioButton1)
        self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton2, self.RadioButton2)
        self.text_top01 = wx.StaticText(self, -1, '邻近值K:', style=wx.TE_LEFT, pos=(20, 35))
        self.textContents01 = wx.TextCtrl(self, style=wx.TE_LEFT, pos=(85, 30), size=(100, 23))
        self.textContents11 = wx.TextCtrl(self, style=wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY, pos=(100, 80),size=(390, 160),value = "结果摘要：\n")    #value = "结果显示："
        # self.textContents01.SetBackgroundColour('#F7F7F7')
        # self.textContents11.SetBackgroundColour('#F7F7F7')

        self.textContents01.AppendText("3")
        self.textContents01.Enable(False)
        # button2 = wx.Button(self, -1, '添加', pos=(350, 279),size=(100, 30))
        button3 = wx.Button(self, -1, '重置', pos=(169, 265),size=(100, 30))
        button4 = wx.Button(self, -1, '取消', pos=(449, 265),size=(100, 30))
        button5 = wx.Button(self, -1, '开始', pos=(29, 265),size=(100, 30))
        button6 = wx.Button(self, -1, '数据',  pos=(309, 265),size=(100, 30))
        # self.Bind(wx.EVT_BUTTON, self.On_Button2, button2)
        self.Bind(wx.EVT_BUTTON, self.On_Button3, button3)
        self.Bind(wx.EVT_BUTTON, self.On_Button4, button4)
        self.Bind(wx.EVT_BUTTON, self.On_Button5, button5)
        self.Bind(wx.EVT_BUTTON, self.On_Button6, button6)

        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False)# font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL,False, u'FZShuTi')
        font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL,False)
        font2 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        # button1.SetFont(font)
        # button2.SetFont(font)
        button3.SetFont(font)
        button4.SetFont(font)
        button5.SetFont(font)
        button6.SetFont(font)
        self.textContents01.SetFont(font1)
        self.textContents11.SetFont(font2)
        self.text_top01.SetFont(font1)
#重置
    def On_Button3(self, event):
        if self.RadioButton1 and self.RadioButton2:
            self.RadioButton1.Destroy()
            self.RadioButton2.Destroy()
            self.RadioButton1 = wx.RadioButton(self, -1, "默认设置", pos=(10, 5), size=(100, 20), style=wx.RB_GROUP)
            self.RadioButton2 = wx.RadioButton(self, -1, "自定义", pos=(110, 5), size=(100, 20))
            self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton1, self.RadioButton1)
            self.Bind(wx.EVT_RADIOBUTTON, self.On_RadioButton2, self.RadioButton2)
            self.textContents01.Enable(False)
        if self.textContents01:
            self.textContents01.Clear()
            self.textContents01.AppendText(k)
        if self.textContents11:
            self.textContents11.SetForegroundColour('black')
            self.fonta5 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
            self.textContents11.SetFont(self.fonta5)
            self.textContents11.SetValue("结果摘要：\n")
#取消
    def On_Button4(self, event):
        sys.exit(0)
#开始
    def On_Button5(self, event):
        self.fontb5 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        if self.textContents01.GetValue()=="" :
            # # easygui.msgbox("窗口不能为空!", title="错误提示")
            self.textContents11.Clear()
            # self.textContents11.SetForegroundColour('red')
            # self.textContents11.SetFont(self.fontb5)
            # self.textContents11.AppendText("K值窗口不能为空\n\n请按照规定格式输入K值!\n")
            wx.MessageBox("K值窗口不能为空\n\n请按照规定格式输入K值!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        K_num=self.textContents01.GetValue()
        if KNN_Model.is_float(K_num)==1:
            self.textContents11.Clear()
            wx.MessageBox("K值不能为小数\n\n请重新输入!\n", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if K_num.isalpha()== True:
            self.textContents11.Clear()
            wx.MessageBox("请按照规定格式输入K值\n\n请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if int(K_num)%2==0 :
            self.textContents11.Clear()
            wx.MessageBox("K值应为奇数，不能为偶数\n\n请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if int(K_num)<0:
            self.textContents11.Clear()
            wx.MessageBox("K值应为奇数，不能为偶数\n\n请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        self.Counte = 0
        FP = open('data\datingTestSet2.txt', 'r')
        for line in FP:
            self.Counte = self.Counte + 1
        FP.close()
        if int(K_num)>self.Counte:
            self.textContents11.Clear()
            wx.MessageBox("数据库中数据量为"+str(self.Counte)+"\n\n您输入的K值已经超过了数据总数\n\n请重新输入!\n", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        self.a = A
        self.b = B
        self.c = num
        self.K = self.textContents01.GetValue()
        expected_data = [float(self.a), float(self.b),float(self.c)]

        fooddata = KNN_Model.getdata('data\datingTestSet2.txt')
        self.flag = KNN_Model.KNN_arithm(fooddata, expected_data, int(self.K), 1)
        self.textContents11.SetForegroundColour('black')
        self.fontb51 = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        self.textContents11.SetFont(self.fontb51)
        self.Q,self.W,self.E = KNN_Model.KNN_arithm(fooddata, expected_data, int(self.K), 0)

        if self.flag ==0:
            self.textContents11.Clear()
            self.textContents11.SetValue('您输入的值为：'+str(K_num)+"\n"+"结果为：1\n\n"+"在"+str(K_num)+"个数据中\n"+
                                         "类一有"+str(self.Q)+"个实例\n"+
                                         "类二有"+str(self.W)+"个实例\n"+
                                         "类三有"+str(self.E)+"个实例\n")
        elif self.flag==1:
            self.textContents11.Clear()
            self.textContents11.SetValue('您选择的值为：'+str(K_num)+"\n"+"结果为：2\n\n"+"在"+str(K_num)+"个数据中\n"+
                                         "类一有"+str(self.Q)+"个实例\n"+
                                         "类二有"+str(self.W)+"个实例\n"+
                                         "类三有"+str(self.E)+"个实例\n")
        elif self.flag==2:
            self.textContents11.Clear()
            self.textContents11.SetValue('您选择的值为：'+str(K_num)+"\n"+"结果为：3\n\n"+"在"+str(K_num)+"个数据中\n"+
                                         "类一有"+str(self.Q)+"个实例\n"+
                                         "类二有"+str(self.W)+"个实例\n"+
                                         "类三有"+str(self.E)+"个实例\n")
        else:
            self.textContents11.Clear()
            self.textContents11.SetValue('您的K值无法进行判别分类')
        Coordinate1.main(self.flag+1)
#数据
    def On_Button6(self, event):
        self.Counte1 = 0
        FP = open('data\datingTestSet2.txt', 'r')
        for line in FP:
            self.Counte1 = self.Counte1 + 1
        FP.close()
        self.textContents11.Clear()
        self.textContents11.SetForegroundColour('black')
        self.fontb35 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        self.textContents11.SetFont(self.fontb35)
        self.textContents11.AppendText('\t\t==数据信息==\n 属性1\t  属性2\t   \t 属性3\t       类别\n')
        fp = open('data\datingTestSet2.txt', 'r')
        for line in fp:
            self.textContents11.write(line + ' ')
        fp.close()
        self.textContents11.AppendText('经计算：\n 共有'+str(self.Counte1)+'个数据\n')
#默认设置
    def On_RadioButton1(self, event):
        self.textContents01.Clear()
        self.textContents01.AppendText(k)
        self.textContents01.Enable(False)
#自定义
    def On_RadioButton2(self, event):
        if self.textContents01:
            self.textContents01.SetBackgroundColour('white')
            self.textContents01.Enable(True)



#第二选项卡
class PageTwo(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        Tapete = wx.Image('KNN\\Tapete2_1.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()  # 把这个图片的内容妆转化为这个pic 变量。
        Liniendiagramm = wx.Image('KNN\\Liniendiagramm.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        Aktualisieren = wx.Image('KNN\\Aktualisieren.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        abc = wx.Image('KNN\\abc.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.text_top11 = wx.StaticText(self, -1, '重置', style=wx.TE_LEFT, pos=(342,135))
        self.text_top22 = wx.StaticText(self, -1, '预测', style=wx.TE_LEFT, pos=(470, 135))
        self.text_top33 = wx.StaticText(self, -1, '坐标', style=wx.TE_LEFT, pos=(342, 255))
        self.text_top44 = wx.StaticText(self, -1, '返回', style=wx.TE_LEFT, pos=(470,255))
        self.textContents111 = None
        self.text2 = None
        self.textc2 = None
        self.text2_1 = None
        self.textc2_1 = None
        self.textc2_2 = None
        self.text2_2 = None
        self.text2_3 = None
        self.textc2_3 = None
        self.textb2 = None
        self.textb2_1 = None
        self.listbox2 = None
        self.textContents1=None
        self.textContents1small = None
        self.button1 = wx.BitmapButton(self, -1,Tapete, pos=(450, 50))  # 固定的写法使用图片按键，并且命名 为 self.button
        self.button4 = wx.BitmapButton(self, -1, Liniendiagramm, pos=(320, 170))
        self.button6 = wx.BitmapButton(self, -1, Aktualisieren, pos=(320, 50))
        self.button8 = wx.BitmapButton(self, -1, abc, pos=(450, 170))
        self.Bind(wx.EVT_BUTTON, self.TapeteBild, self.button1)
        self.Bind(wx.EVT_BUTTON, self.LiniendiagrammBild, self.button4)
        self.Bind(wx.EVT_BUTTON, self.AktualisierenBild, self.button6)
        self.Bind(wx.EVT_BUTTON, self.abcBild, self.button8)
        self.button1.SetDefault()
        self.button4.SetDefault()
        self.button6.SetDefault()
        self.button8.SetDefault()
        self.textContents1 = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY, pos=(20, 40), size=(270, 255), value="结果显示：")
        font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.textContents1.SetFont(font1)
#预测
    def TapeteBild(self, event):
        # font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        if self.textContents1:
            self.textContents1.Destroy()
        if not self.textContents1small:
            self.textContents1small = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY,
                                             pos=(20, 40), size=(270, 100), value="结果显示：")
            font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
            self.textContents1small.SetFont(font1)
        if not self.text2:
            self.text2 = wx.StaticText(self, -1, u'属性值1:', (50, 160), (50, -1), wx.ALIGN_CENTER)
        if not self.text2_1:
            self.text2_1 = wx.StaticText(self, -1, u'属性值2:', (50, 190), (50, -1), wx.ALIGN_CENTER)
        if not self.text2_2:
            self.text2_2 = wx.StaticText(self, -1, u'属性值3:', (50, 220), (50, -1), wx.ALIGN_CENTER)
        if not self.text2_3:
            self.text2_3 = wx.StaticText(self, -1, u'邻近值K:', (50, 250), (50, -1), wx.ALIGN_CENTER)
        if not self.textc2:
            self.textc2 = wx.TextCtrl(self, pos=(140, 155), size=(100, 25))
            self.textc2.AppendText("72993")
        if not self.textc2_1:
            self.textc2_1 = wx.TextCtrl(self, pos=(140, 185), size=(100, 25))
            self.textc2_1.AppendText("10.141740")
        if not self.textc2_2:
            self.textc2_2 = wx.TextCtrl(self, pos=(140, 215), size=(100, 25))
            self.textc2_2.AppendText("1.032955")
        if not self.textc2_3:
            self.textc2_3 = wx.TextCtrl(self, style=wx.TE_LEFT, pos=(140, 245), size=(100, 25))
            self.textc2_3.AppendText("3")
        if not self.textb2:
            self.textb2 = wx.Button(self, -1, '预测', pos=(50, 275), size=(70, 25))
            self.Bind(wx.EVT_BUTTON, self.On_Button2_1, self.textb2)
        if not self.textb2_1:
            self.textb2_1 = wx.Button(self, -1, '默认', pos=(170, 275), size=(70, 25))
            self.Bind(wx.EVT_BUTTON, self.On_ButtonLeer, self.textb2_1)
#重置
    def AktualisierenBild(self, event):
        if self.text2:
            self.text2.Destroy()
        if self.textContents1small:
            self.textContents1small.Destroy()
        if self.textc2_2:
            self.textc2_2.Destroy()
        if self.text2_3:
            self.text2_3.Destroy()
        if self.text2_2:
            self.text2_2.Destroy()
        if self.textc2_3:
            self.textc2_3.Destroy()
        if self.text2_1:
            self.text2_1.Destroy()
        if self.textc2:
            self.textc2.Destroy()
        if self.textc2_1:
            self.textc2_1.Destroy()
        if self.textb2:
            self.textb2.Destroy()
        if self.textb2_1:
            self.textb2_1.Destroy()
        if self.listbox2:
            self.listbox2.Destroy()
        if self.textContents1:
            font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
            self.textContents1.SetFont(font1)
            self.textContents1.SetValue("结果显示：")
        if not self.textContents1:
            self.textContents1 = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY,
                                             pos=(20, 40), size=(270, 255), value="结果显示：")
            font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
            self.textContents1.SetFont(font1)
#坐标
    def LiniendiagrammBild(self, event):
        coordinate.main()
#返回
    def abcBild(self,event):
        if self.text2:
            self.text2.Destroy()
        if self.textContents1small:
            self.textContents1small.Destroy()
        if self.textc2_2:
            self.textc2_2.Destroy()
        if self.text2_3:
            self.text2_3.Destroy()
        if self.text2_2:
            self.text2_2.Destroy()
        if self.text2_1:
            self.text2_1.Destroy()
        if self.textc2:
            self.textc2.Destroy()
        if self.textc2_1:
            self.textc2_1.Destroy()
        if self.textb2:
            self.textb2.Destroy()
        if self.textb2_1:
            self.textb2_1.Destroy()
        if self.listbox2:
            self.listbox2.Destroy()
        if self.textContents1:
            font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
            self.textContents1.SetFont(font1)
            self.textContents1.SetValue("结果显示：")
        if not self.textContents1:
            self.textContents1 = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY,
                                             pos=(20, 40), size=(270, 255), value="结果显示：")
            font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
            self.textContents1.SetFont(font1)
            self.textContents1.SetBackgroundColour('#F7F7F7')
        nb.SetSelection(0)
#预测按键small
    def On_Button2_1(self, event):
        self.fontb5 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False)
        if self.textc2_3.GetValue() == "":
            self.textc2_3.Clear()
            wx.MessageBox("K值窗口不能为空\n\n请按照规定格式输入K值!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        K_num = self.textc2_3.GetValue()
        if KNN_Model.is_float(K_num) == 1:
            self.textc2_3.Clear()
            wx.MessageBox("K值不能为小数\n\n请重新输入!\n", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if K_num.isalpha() == True:
            self.textc2_3.Clear()
            wx.MessageBox("请按照规定格式输入K值\n\n请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if int(K_num) % 2 == 0:
            self.textc2_3.Clear()
            wx.MessageBox("K值应为奇数，不能为偶数\n\n请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if int(K_num) < 0:
            self.textc2_3.Clear()
            wx.MessageBox("K值应为奇数，不能为偶数\n\n请重新输入!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        if self.textc2.GetValue() == "" or self.textc2_1.GetValue() == "" or self.textc2_2.GetValue() == "":
            wx.MessageBox("不能为空!", "警告", wx.OK | wx.ICON_INFORMATION)
            return
        self.Counte = 0
        FP = open('data\datingTestSet2.txt', 'r')
        for line in FP:
            self.Counte = self.Counte + 1
        FP.close()
        if int(K_num) > self.Counte:
            self.textc2_3.Clear()
            wx.MessageBox("数据库中数据量为" + str(self.Counte) + "\n\n您输入的K值已经超过了数据总数\n\n请重新输入!\n", "警告",
                          wx.OK | wx.ICON_INFORMATION)
            return
        self.aa = self.textc2.GetValue()
        self.bb = self.textc2_1.GetValue()
        self.cc = self.textc2_2.GetValue()
        self.dd = self.textc2_3.GetValue()
        expected_data1 = [float(self.aa), float(self.bb), float(self.cc)]
        fooddata1 = KNN_Model.getdata("data\datingTestSet2.txt")
        print int(self.dd)
        self.flag1 = str(KNN_Model.KNN_arithm(fooddata1, expected_data1, int(self.dd), 1) + 1)
        print self.flag1
        self.textContents1small.Clear()
        if self.flag1 =='1':
            self.textContents1small.SetValue("所属类为：1\n")
        elif self.flag1=='2':
            self.textContents1small.SetValue("所属类为：2\n")
        elif self.flag1=='3':
            self.textContents1small.SetValue("所属类为：3\n")
        else:
            self.textContents1small.SetValue('您的K值无法进行判别分类')
        self.textContents1small.AppendText("属性1：" + str(self.aa) + "\n")
        self.textContents1small.AppendText("属性2：" + str(self.bb) + "\n")
        self.textContents1small.AppendText("属性3：" + str(self.cc) + "\n")
#默认按键small
    def On_ButtonLeer(self, event):
        if self.textc2:
            self.textc2.Clear()
            self.textc2.AppendText("72993")
        if self.textc2_1:
            self.textc2_1.Clear()
            self.textc2_1.AppendText("10.141740")
        if self.textc2_2:
            self.textc2_2.Clear()
            self.textc2_2.AppendText("1.032955")
        if self.textc2_3:
            self.textc2_3.Clear()
            self.textc2_3.AppendText(k)



#第三选项卡
class PageThree(wx.Panel):
    def __init__(self,parent):
        font3_1 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL)
        wx.Panel.__init__(self,parent)
        try:
            image_file = 'KNN\\Tapete.jpg'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))
        except IOError:
            print 'Image file %s not found' % image_file
            raise SystemExit
        self.textContents001 = wx.TextCtrl(self.bitmap, style=wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY, pos=(20, 20), size=(300, 270))
        # self.textContents001.SetTransparent(200)  # 设置透明
        self.textContents001.SetBackgroundColour('#F7F7F7')
        self.textb3_1 = wx.Button(self.bitmap, -1, '算法简介', pos=(350, 40), size=(200, 30))
        self.textb3_2 = wx.Button(self.bitmap, -1, '算法流程', pos=(350, 80), size=(200, 30))
        self.textb3_3= wx.Button(self.bitmap, -1, '算法优点', pos=(350, 120), size=(200, 30))
        self.textb3_4 = wx.Button(self.bitmap, -1, '算法缺点', pos=(350, 160), size=(200, 30))
        self.textb3_5 = wx.Button(self.bitmap, -1, '改进策略', pos=(350, 200), size=(200, 30))
        self.textb3_6 = wx.Button(self.bitmap, -1, '返回主页', pos=(350, 240), size=(200, 30))
        self.Bind(wx.EVT_BUTTON, self.On_Button3_1, self.textb3_1)
        self.Bind(wx.EVT_BUTTON, self.On_Button3_2, self.textb3_2)
        self.Bind(wx.EVT_BUTTON, self.On_Button3_3, self.textb3_3)
        self.Bind(wx.EVT_BUTTON, self.On_Button3_4, self.textb3_4)
        self.Bind(wx.EVT_BUTTON, self.On_Button3_5, self.textb3_5)
        self.Bind(wx.EVT_BUTTON, self.On_Button3_6, self.textb3_6)
        self.textContents001.SetFont(font3_1)

        font3_1 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'STXingkai')
        self.textContents001.SetFont(font3_1)
        font3_2 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'STXingkai')
        self.textb3_1.SetFont(font3_2)
        self.textb3_2.SetFont(font3_2)
        self.textb3_3.SetFont(font3_2)
        self.textb3_4.SetFont(font3_2)
        self.textb3_5.SetFont(font3_2)
        self.textb3_6.SetFont(font3_2)


    # 算法简介
    def On_Button3_1(self, event):
        self.textContents001.Clear()
        self.textContents001.AppendText('          '
                                        '==KNN近邻算法==' + '\n' + '        K最近邻(k-Nearest Neighbor，KNN)分类算法，'
                                        '是一个理论上比较成熟的方法，也是最简单的机器学习算法之一。该方法的思路'
                                        '是：如果一个样本在特征空间中的k个最相似(即特征空间中最邻近)的样本中的大'
                                        '多数属于某一个类别，则该样本也属于这个类别。KNN算法中，所选择的邻居都是'
                                        '已经正确分类的对象。该方法在定类决策上只依据最邻近的一个或者几个样本的'
                                        '类别来决定待分样本所属的类别。 KNN方法虽然从原理上也依赖于极限定理，但'
                                        '在类别决策时，只与极少量的相邻样本有关。由于KNN方法主要靠周围有限的邻近'
                                        '的样本，而不是靠判别类域的方法来确定所属类别的，因此对于类域的交叉或重叠'
                                        '较多的待分样本集来说，KNN方法较其他方法更为适合。')
    # 算法流程
    def On_Button3_2(self, event):
        self.textContents001.Clear()
        self.textContents001.AppendText('          '
                                        '==KNN近邻算法==' + '\n' + '①准备数据，对数据进行预处理'+ '\n' + '②选用合'
                                        '适的数据结构存储训练数据和测试元组'+ '\n' + '③设定参数，如k'+ '\n' + '④维'
                                        '护一个大小为k的的按距离由大到小的优先级队列，用于存储最近邻训练元组。随机从'
                                        '训练元组中选取k个元组作为初始的最近邻元组，分别计算测试元组到这k个元组的距离，'
                                        '将训练元组标号和距离存入优先级队列'+ '\n' + '⑤遍历训练元组集，计算当前训练'
                                        '元组与测试元组的距离，将所得距离L 与优先级队列中的最大距离Lmax'+ '\n' + '⑥进'
                                        '行比较。若L>=Lmax，则舍弃该元组，遍历下一个元组。若L < Lmax，删除优先级队列中'
                                        '最大距离的元组，将当前训练元组存入优先级队列。'+ '\n' + '⑦遍历完毕，计算优先'
                                        '级队列中k 个元组的多数类，并将其作为测试元组的类别。'+ '\n' + '⑧测试元组集测'
                                        '试完毕后计算误差率，继续设定不同的k值重新进行训练，最后取误差率最小的k 值。')

    # 算法优点
    def On_Button3_3(self, event):
        self.textContents001.Clear()
        self.textContents001.AppendText('          '
                                        '==KNN近邻算法==' + '\n' + '①简单，易于理解，易于实现，无需估计参数，无需训练；'
                                        ''+ '\n' + '②适合对稀有事件进行分类；'+ '\n' + '③特别适合于多分类问题(multi-m'
                                        'odal,对象具有多个类别标签)， kNN比SVM的表现要好。')
    #算法缺点
    def On_Button3_4(self, event):
        self.textContents001.Clear()
        self.textContents001.AppendText('          '
                                        '==KNN近邻算法==' + '\n' + '    该算法在分类时有个主要的不足是，当样本不平衡时，'
                                        '如一个类的样本容量很大，而其他类样本容量很小时，有可能导致当输入一个新样本时，'
                                        '该样本的K个邻居中大容量类的样本占多数。 该算法只计算“最近的”邻居样本，某一类'
                                        '的样本数量很大，那么或者这类样本并不接近目标样本，或者这类样本很靠近目标样本。'
                                        '无论怎样，数量并不能影响运行结果。该方法的另一个不足之处是计算量较大，因为对每'
                                        '一个待分类的文本都要计算它到全体已知样本的距离，才能求得它的K个最近邻点。可理解'
                                        '性差，无法给出像决策树那样的规则。')
    #改进策略
    def On_Button3_5(self, event):
        self.textContents001.Clear()
        self.textContents001.AppendText('          '
                                        '==KNN近邻算法==' + '\n' + '    kNN算法因其提出时间较早，随着其他技术的不断更新'
                                        '和完善，kNN算法的诸多不足之处也逐渐显露，因此许多kNN算法的改进算法也应运而生。'
                                        '针对以上算法的不足，算法的改进方向主要分成了分类效率和分类效果两方面。分类效率：'
                                        '事先对样本属性进行约简，删除对分类结果影响较小的属性，快速的得出待分类样本的类'
                                        '别。该算法比较适用于样本容量比较大的类域的自动分类，而那些样本容量较小的类域采'
                                        '用这种算法比较容易产生误分。分类效果：采用权值的方法（和该样本距离小的邻居权值'
                                        '大）来改进，Han等人于2002年尝试利用贪心法，针对文件分类实做可调整权重的k最近邻'
                                        '居法WAkNN (weighted adjusted k nearest neighbor)，以促进分类效果；而Li等人于20'
                                        '04年提出由于不同分类的文件本身有数量上有差异，因此也应该依照训练集合中各种分类'
                                        '的文件数量，选取不同数目的最近邻居，来参与分类。')
    #返回主页
    def On_Button3_6(self, event):
        nb.SetSelection(0)

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self,None,title="中医药数据分析平台",size=(600,400),style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))

        self.statusbar=self.CreateStatusBar()
        self.statusbar.SetStatusText(u"中医药数据分析平台：@尚智祥Jonas(2018/11/27)")
        self.statusbar.SetBackgroundColour('white')  # 设置背景颜色
        setImg = wx.Image('KNN\\300.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        setIcon = wx.Icon(setImg)
        self.SetIcon(setIcon)
        #Here we create a panel and a notebook on the panel
        p=wx.Panel(self)
        p.SetBackgroundColour('White')
        global nb
        nb=wx.Notebook(p)
        #create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)
        # page4 = PageFour(nb)
        #add the pages to the notebook with the label to show the tab
        nb.AddPage(page1,"参数设置")
        nb.AddPage(page2, "功能面板")
        nb.AddPage(page3, "其它信息")
        # nb.AddPage(page4, "数据坐标")
        #finally,put the notebook in a sizer for the panel to manage
        #the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb,1,wx.EXPAND)
        p.SetSizer(sizer)

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1)
        frame.Bind(wx.EVT_CLOSE, self.OnCloseWindow, frame)
        frame.Show()
        frame.Center()
        frame.SetMaxSize((600,400))
        frame.SetMinSize((600,400))
        self.SetTopWindow(frame)
        self.frame = frame
    	return 1
    def OnCloseWindow(self,event):
        dlg = wx.MessageDialog(None,'Exit , Are you sure ?', 'Confirmation',wx.YES_NO|wx.ICON_QUESTION)
        retCode = dlg.ShowModal()
        if(retCode == wx.ID_YES):
            self.frame.Show(False)
            sys.exit(0)
        else:
            pass



def main():
    app = MyApp(0)
#    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
