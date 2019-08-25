# coding=utf-8
# from __future__ import division
import numpy
import math
import wx
import ctypes  # An included library with Python install.
def getdata(medience_file):
    data = []
    lines = open(medience_file, 'r')
    for line in lines:
        data.append(list(line.strip(' ').split('\t')))##strip删除字符串中的空格##split按某个字符分割
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            data[i][j] = float(data[i][j])
    lines.close()
    return data

def KNN_arithm(data, expected_data,k,FLAG):#FLAG默认等于1
    distance = []
    list1=[]
    food_index = 0
    for l in data:
        list1 += [l[3]]
    for i in range(0, len(data)):
        # food.append(math.sqrt(
        #     (numpy.square(expected_data[0] - data[i][0]) + numpy.square(expected_data[1] - data[i][1])+numpy.square(expected_data[2] - data[i][2]))))
        distance.append(math.sqrt(
            (numpy.square(expected_data[0] - data[i][0]) + numpy.square(expected_data[1] - data[i][1])+numpy.square(expected_data[2] - data[i][2]))))
        # list1[i]=data[i][3]
    z = list(zip(distance, list1))#将两个数组合并成一个二维数组
    z.sort(reverse=False)#steigen
    # k = int(len(distance) / 2) + 1
    # distance = distance[0:k - 1]#Von 1 bis zu k-1 besuchen
    a=0
    b=0
    c=0
    # for i in range(0, len(data)):
    #     data[i][3] = int(data[i][3])
    #     print z
    for i in range(0, k):
        if z[i][1]==1:
            a=a+1
        elif z[i][1]==2:
            b=b+1
        else:
            c=c+1
    # final = [a, b, c]
    # final_index = final.index(max(final))

    if FLAG==0:
        return a,b,c

    print a
    print b
    print c
    if max(a,b,c) == a:
        return 0
    elif max(a,b,c) == b:
        return 1
    elif max(a,b,c) == c:
        return 2
    else:
        return 3

# def Mbox(title, text, style):
#     return ctypes.windll.user32.MessageBoxW(0, text, title, style)
def readFile(filepath):
    with open(filepath, "r") as f:
        while (True):
            yield f.readline().strip(' ')
def is_float(str):
    if str.count('.') == 1: #小数有且仅有一个小数点
        left = str.split('.')[0]  #小数点左边（整数位，可为正或负）
        right = str.split('.')[1]  #小数点右边（小数位，一定为正）
        lright = '' #取整数位的绝对值（排除掉负号）
        if str.count('-') == 1 and str[0] == '-': #如果整数位为负，则第一个元素一定是负号
            lright = left.split('-')[1]
        elif str.count('-') == 0:
            lright = left
        else:
            return 0
        if right.isdigit() and lright.isdigit(): #判断整数位的绝对值和小数位是否全部为数字
            return 1
        else:
            return 0
    else:
        return 0
def KNNabc(data, expected_data,k):
    distance = []
    list1=[]
    food_index = 0
    for l in data:
        list1 += [l[3]]
    for i in range(0, len(data)):
        # food.append(math.sqrt(
        #     (numpy.square(expected_data[0] - data[i][0]) + numpy.square(expected_data[1] - data[i][1])+numpy.square(expected_data[2] - data[i][2]))))
        distance.append(math.sqrt(
            (numpy.square(expected_data[0] - data[i][0]) + numpy.square(expected_data[1] - data[i][1])+numpy.square(expected_data[2] - data[i][2]))))
        # list1[i]=data[i][3]
    z = list(zip(distance, list1))#将两个数组合并成一个二维数组
    z.sort(reverse=False)#steigen
    # k = int(len(distance) / 2) + 1
    # distance = distance[0:k - 1]#Von 1 bis zu k-1 besuchen
    a=0
    b=0
    c=0
    # for i in range(0, len(data)):
    #     data[i][3] = int(data[i][3])
    #     print z
    for i in range(0, k):
        if z[i][1]==1:
            a=a+1
        elif z[i][1]==2:
            b=b+1
        else:
            c=c+1
    return a,b,c

#2维平面图
def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result