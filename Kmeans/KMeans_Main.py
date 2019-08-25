# coding: utf-8
import matplotlib
matplotlib.use("WXAgg")
matplotlib.rcParams['figure.figsize'] = [7, 4.5]
import wx
from numpy import *
import wx.py.images as images
import KMeans_Model
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
class MyPanel(wx.Panel):
    def __init__(self,parent,data):
        wx.Panel.__init__(self,parent=parent, id=-1)
        data1=mat(data)
        self.main_data=mat(data)
        self.draw(1, data1)
    def read(self,image):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.imshow(image)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
    def draw(self, x, data,center=[]):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        if x==1:
            self.axes.scatter(array(data[:, 0]), array(data[:, 1]), s=25, alpha=1, color='black')
        else:
            mark = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
            for i in range(len(data)):
                markIndex = int(data[i, 0])
                self.axes.scatter(self.main_data[i, 0], self.main_data[i, 1], s=25, alpha=1, c=mark[markIndex])
        if x==2:
            mark = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
            for i in range(len(center)):
                x=array(center[i, 0])
                y=array(center[i, 1])
                self.axes.scatter(x, y, s=256, marker='+',c=mark[i])
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
class MyPanel1(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self, parent=parent, id=id)
        self.font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, False, '宋体')
        self.t1 = wx.TextCtrl(self, size=(786, 520), style=wx.TE_MULTILINE)
        self.t1.AppendText('1.什么是聚类分析\n')
        self.t1.AppendText('    聚类分析是在数据中发现数据对象之间的关系，将数据进行分组，组内的相似性越大，组间的差别越大，则聚类效果越好。\n')
        self.t1.AppendText('2.基本的聚类分析算法\n')
        self.t1.AppendText('    (1).K均值： 基于原型的、划分的距离技术，它试图发现用户指定个数(K)的簇。\n')
        self.t1.AppendText('    (2).凝聚的层次距离： 思想是开始时，每个点都作为一个单点簇，然后，重复的合并两个最靠近的簇，直到尝试单个、包含所有点的簇。。\n')
        self.t1.AppendText('    (3).DBSCAN: 一种基于密度的划分距离的算法，簇的个数有算法自动的确定，低密度中的点被视为噪声而忽略，因此其不产生完全聚类。\n')
        self.t1.AppendText('3.传统K-Means算法\n')
        self.t1.AppendText('    优点:\n    (1)易于实现 \n')
        self.t1.AppendText('    缺点:\n    (1).在大规模数据收敛慢,当样本数量比较大时计算的开销也会非常大. \n')
        self.t1.AppendText('    (2).局部最优解，K-Means的初始重心位置是随机选择的。有时，如果运气不好，随机选择的重心会导致K-Means陷入局部最优解。\n')
        self.t1.AppendText('    (3).K-Means算法对初始选取的聚类中心点是敏感的，不同的随机种子点得到的聚类结果完全不同 \n')
        self.t1.AppendText('4.改进后的二分K-均值(bisecting K-means)\n')
        self.t1.AppendText('    优点:\n    (1)二分K均值算法可以加速K-means算法的执行速度，因为它的相似度计算少了.\n')
        self.t1.AppendText('    (2).不受初始化问题的影响，因为这里不存在随机点的选取，且每一步都保证了误差最小.\n')
        self.t1.AppendText('    缺点:\n    (1).由于这个是K-means的改进算法，所以缺点大致与之相同.\n')
        self.t1.SetFont(self.font)
class MyFrame(wx.Frame):
    def __init__(self, main_data,parent=None, id=-1, title='中医药数据分析平台'):
        wx.Frame.__init__(self, parent, id, title, size=(800, 650),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))
        self.main_data=main_data
        self.Center()
        self.font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, False, '宋体')
        self.nb = wx.Notebook(self)
        panel1 = wx.Panel(self.nb, -1)
        self.picture=MyPanel(panel1,self.main_data)
        self.picture.SetPosition((0,70))
        self.picture.SetSize((700,450))
        self.rb1 = wx.RadioButton(panel1, 11, label='默认参数', style = wx.RB_GROUP, pos=(60,10))
        self.rb2 = wx.RadioButton(panel1, 22, label='自定义参数', pos=(350,10))
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
        st1 = wx.StaticText(panel1, -1, 'k(k表示k个聚类中心)：',pos=(60,50))
        self.tc1 = wx.TextCtrl(panel1,pos=(350,45))
        self.Start = wx.Button(panel1, -1, '开始', style=wx.BORDER_MASK, pos=(60, 530),size=(90,30))
        self.Start.SetFont(self.font)
        self.Reset = wx.Button(panel1, -1, '重置', style=wx.BORDER_MASK, pos=(190, 530),size=(90,30))
        self.Reset.SetFont(self.font)
        self.Store = wx.Button(panel1, -1, '保存', style=wx.BORDER_MASK, pos=(320, 530), size=(90, 30))
        self.Store.SetFont(self.font)
        self.Cancel = wx.Button(panel1, -1, '取消', style=wx.BORDER_MASK, pos=(450, 530),size=(90,30))
        self.Cancel.SetFont(self.font)
        self.Import = wx.Button(panel1, -1, '导入', style=wx.BORDER_MASK, pos=(580, 530), size=(90, 30))
        self.Import.SetFont(self.font)
        self.Start.Bind(wx.EVT_BUTTON, self.Start_Modeling)
        self.Reset.Bind(wx.EVT_BUTTON, self.Reset_Value)
        self.Cancel.Bind(wx.EVT_BUTTON, self.Close_Program)
        self.Store.Bind(wx.EVT_BUTTON, self.Store_Image)
        self.Import.Bind(wx.EVT_BUTTON, self.Read_Image)
        self.reset()
        self.nb.InsertPage(0, panel1, '参数设置', True)
        panel4 = MyPanel1(self.nb,-1)
        self.nb.InsertPage(1, panel4, '其他', False)
        statusbar = self.CreateStatusBar()
        statusbar.SetStatusText('版权所有:计算机学院B313')
    def OnRadiogroup(self, event):
        if event.GetEventObject() == self.rb1:
            self.tc1.SetValue('4')
            self.tc1.Enable(False)
        else:
            self.tc1.SetValue('')
            self.tc1.Enable(True)
    def Start_Modeling(self, event):
        a=self.tc1.GetValue().strip()
        if a=='':
            wx.MessageBox("k值不可为空", "警告", wx.OK | wx.ICON_INFORMATION)
        else:
            if a.isalpha():
                wx.MessageBox("k值不能为字母", "小提示", wx.OK | wx.ICON_INFORMATION)
            else:
                if '.'in a:
                    wx.MessageBox("k值不能为小数", "小提示", wx.OK | wx.ICON_INFORMATION)
                else:
                    if a.isdigit():
                        if int(a)>8:
                            wx.MessageBox("由于界面大小的原因我建议k值小于等于8，也便于结果可视化", "小提示", wx.OK | wx.ICON_INFORMATION)
                        else:
                            dataMat = mat(self.main_data)
                            centList, myNewAssments = KMeans_Model.biKmeans(dataMat, int(self.tc1.GetValue()))
                            self.picture.draw(2,myNewAssments,centList)
                    else:
                        wx.MessageBox("请输入数字", "小提示", wx.OK | wx.ICON_INFORMATION)
    def Reset_Value(self, event):
        self.reset()
        data = mat(self.main_data)
        self.picture.draw(1, data)
    def reset(self):
        self.tc1.SetValue('4')
        self.tc1.Enable(False)
        self.rb1.SetValue(True)
    def Close_Program(self, event):
        sys.exit()
    def Store_Image(self, event):
        dlg = wx.FileDialog(self, message="Find somewwhere to Save file", defaultFile="", defaultDir='C:',
                            wildcard='PNG files (*.png)|*.png', style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            wherefile = dlg.GetDirectory() + '\\' + dlg.GetFilename()
            self.picture.figure.savefig(wherefile)
        dlg.Destroy()
    def Read_Image(self, event):#有个缺陷读完后不知道参数，这个目前想不到
        dlg = wx.FileDialog(self, message="Find a file", defaultFile="", defaultDir='C:',
                            wildcard='PNG files (*.png)|*.png', style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            wherefile = dlg.GetDirectory() + '\\' + dlg.GetFilename()
            myimage=matplotlib.image.imread(wherefile)
            self.picture.read(myimage)
        dlg.Destroy()
def main(main_data):
    app = wx.App()
    frame = MyFrame(main_data)
    frame.Show()
    app.MainLoop()
