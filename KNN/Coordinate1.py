#!/usr/bin/python
#-*- coding: utf-8 -*-
import numpy as np
import re
import wx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class abc(wx.Panel):
    def __init__(self, parent, id, Flag):
        wx.Panel.__init__(self, parent, id)
        def readFile(filepath):
            with open(filepath, "r") as f:
                while (True):
                    yield f.readline().strip()
        filepath = "data\datingTestSet2.txt"
        # list = open(filepath,"r").readlines().strip()
        time = 0
        self.flag=Flag
        list = []
        XY = np.zeros((2, 1000))
        for i in readFile(filepath):
            if (time >= 1000):
                break
            li = [float(j) for j in re.split('\t', i)]
            XY[0][time] = li[0]
            XY[1][time] = li[1]
            time = time + 1
        # print (XYZ)
        fig = plt.figure()
        # ax = plt.subplot(111, projection='3d')
        plt.scatter(XY[0][:500], XY[1][:500], c='y')
        plt.scatter(XY[0][100:200], XY[1][100:200], c='r')
        plt.scatter(XY[0][200:400], XY[1][200:400], c='g')
        plt.scatter(72993, 10.141740, c='b')
        if self.flag==1:
            plt.scatter(72993, 10.141740, c='y',linewidths=30,marker='o')
        elif self.flag==2:
            plt.scatter(72993, 10.141740, c='r', linewidths=30, marker='o')
        else:
            plt.scatter(72993, 10.141740, c='g', linewidths=30, marker='o')
        bbox_props = dict(boxstyle="round", fc="w", ec="0.1", alpha=1)
        t = plt.text(60000,6, "Direction", ha="center", va="center", rotation=40, size=10, bbox=bbox_props)
        bb = t.get_bbox_patch()
        bb.set_boxstyle("rarrow", pad=0.6)
        # NUM=PageOne.number()
        # plt.scatter(72993, 10.141740, c='K',linewidths=60,marker='o')
        # plt.annotate(s='this point is important', xy=(5, 30), xytext=(7, 31),
        #              arrowprops={'arrowstyle': '->'})
        # bbox_props = dict(boxstyle="round", fc="w", ec="0.1", alpha=1)
        # t = plt.text(58888,5.5, "Direction", ha="center", va="center", rotation=40, size=10, bbox=bbox_props)
        # bb = t.get_bbox_patch()
        # bb.set_boxstyle("rarrow", pad=0.6)
        # plt.annotate('y_actual',xy=(55,22),xytext=(7.3,0.025),arrowprops=dict(facecolor='black',shrink=0.05))

        plt.savefig('KNN/bild/test1.jpg')

        try:
            image_file = 'KNN/bild/test1.jpg'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (-30,-50))
            # image_width = to_bmp_image.GetWidth()
            # image_height = to_bmp_image.GetHeight()
            # set_title = '%s %d x %d' % (image_file, to_bmp_image.GetWidth(), to_bmp_image.GetHeight())
            set_title = 'knn'
            parent.SetTitle(set_title)

        except IOError:
            print 'Image file %s not found' % image_file
            raise SystemExit
            # 创建一个按钮
        # self.button = wx.Button(self.bitmap, -1, '确定', pos=(250, 450), size=(100, 30))
        # self.Bind(wx.EVT_BUTTON, self.On_Button, self.button)
        # self.button1 = wx.Button(self.bitmap, -1, '取消', pos=(300, 450), size=(100, 30))
        # self.Bind(wx.EVT_BUTTON, self.Exit, self.button1)


    # def On_Button(self, event):
    #     def readFile(filepath):
    #         with open(filepath, "r") as f:
    #             while (True):
    #                 yield f.readline().strip()
    #     filepath = "datingTestSet2.txt"
    #     # list = open(filepath,"r").readlines().strip()
    #     time = 0
    #     list = []
    #     XY = np.zeros((2, 1000))
    #     for i in readFile(filepath):
    #         if (time >= 1000):
    #             break
    #         li = [float(j) for j in re.split('\t', i)]
    #         XY[0][time] = li[0]
    #         XY[1][time] = li[1]
    #         time = time + 1
    #     # print (XYZ)
    #     fig = plt.figure()
    #     # ax = plt.subplot(111, projection='3d')
    #     plt.scatter(XY[0][:500], XY[1][:500], c='y')
    #     plt.scatter(XY[0][100:200], XY[1][100:200], c='r')
    #     plt.scatter(XY[0][200:400], XY[1][200:400], c='g')
    #     plt.scatter(72993, 10.141740, c='b')
    #     # NUM=PageOne.number()
    #     print 'Flag='
    #     print self.flag
    #     if self.flag==1:
    #         plt.scatter(72993, 10.141740, c='y',linewidths=30,marker='o')
    #     elif self.flag==2:
    #         plt.scatter(72993, 10.141740, c='r', linewidths=30, marker='o')
    #     else:
    #         plt.scatter(72993, 10.141740, c='g', linewidths=30, marker='o')
    #     # plt.annotate(s='this point is important', xy=(5, 30), xytext=(7, 31),
    #     #              arrowprops={'arrowstyle': '->'})
    #     bbox_props = dict(boxstyle="round", fc="w", ec="0.1", alpha=1)
    #     t = plt.text(60000,6, "Direction", ha="center", va="center", rotation=40, size=10, bbox=bbox_props)
    #     bb = t.get_bbox_patch()
    #     bb.set_boxstyle("rarrow", pad=0.6)
    #     # plt.annotate('y_actual',xy=(55,22),xytext=(7.3,0.025),arrowprops=dict(facecolor='black',shrink=0.05))
    #
    #     plt.savefig('./bild/test1.jpg')
    #
    #     try:
    #         image_file = './bild/test1.jpg'
    #         to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    #         self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (-30,-50))
    #         # image_width = to_bmp_image.GetWidth()
    #         # image_height = to_bmp_image.GetHeight()
    #         # set_title = '%s %d x %d' % (image_file, to_bmp_image.GetWidth(), to_bmp_image.GetHeight())
    #
    #     except IOError:
    #         print 'Image file %s not found' % image_file
    #         raise SystemExit
    #         # 创建一个按钮
def main(Flag):
    app = wx.App()
    frame = wx.Frame(None, -1, 'Image', size=(610, 460),style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))
    frame.SetMaxSize((610, 460))
    frame.SetMinSize((610, 460))
    my_panel = abc(frame, -1, Flag)
    frame.Center()
    frame.Show()
    app.MainLoop()