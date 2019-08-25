#!/usr/bin/python
#-*- coding: utf-8 -*-
import numpy as np
import re
import wx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class coordinatemain(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        def readFile(filepath):
            with open(filepath, "r") as f:
                while (True):
                    yield f.readline().strip()

        filepath = "data\datingTestSet2.txt"
        # list = open(filepath,"r").readlines().strip()
        time = 0
        list = []

        XYZ = np.zeros((3, 1000))
        for i in readFile(filepath):
            if (time >= 1000):
                break
            li = [float(j) for j in re.split('\t', i)]
            XYZ[0][time] = li[0]
            XYZ[1][time] = li[1]
            XYZ[2][time] = li[2]
            time = time + 1
        # print (XYZ)
        fig = plt.figure()
        ax = plt.subplot(111, projection='3d')
        ax.scatter(72993, 10.141740, 1.032955, c='b', marker='D')
        ax.scatter(XYZ[0][:500], XYZ[1][:500], XYZ[2][:500], c='y')
        ax.scatter(XYZ[0][100:200], XYZ[1][100:200], XYZ[2][100:200], c='r')
        ax.scatter(XYZ[0][200:400], XYZ[1][200:400], XYZ[2][200:400], c='g')
        ax.scatter(72993, 10.141740, 1.032955, c='b',linewidths=30,marker='o')

        plt.savefig('KNN/bild/test.jpg')

        try:
            image_file = 'KNN/bild/test.jpg'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (-30,-50))
            image_width = to_bmp_image.GetWidth()
            image_height = to_bmp_image.GetHeight()
            # set_title = '%s %d x %d' % (image_file, to_bmp_image.GetWidth(), to_bmp_image.GetHeight())
            set_title = 'knn三维坐标'

            parent.SetTitle(set_title)
        except IOError:
            print 'Image file %s not found' % image_file
            raise SystemExit
            # 创建一个按钮


def main():
    app = wx.App()
    frame = wx.Frame(None, -1, 'Image', size=(610, 460),style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))
    frame.SetMaxSize((610, 460))
    frame.SetMinSize((610, 460))
    my_panel = coordinatemain(frame, -1)
    frame.Center()
    frame.Show()
    app.MainLoop()