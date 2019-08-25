# coding:utf-8
import wx
import Second_interface

class MyFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='中医药数据分析平台'):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU))
        setImg = wx.Image('school.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        setIcon = wx.Icon(setImg)
        self.SetIcon(setIcon)
        self.CenterOnScreen();
        panel = wx.Panel(self, -1)
        self.font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.LIGHT, False, 'Bauhaus 93')
        self.bt1 = wx.Button(panel, -1, 'Partial\nLeast\nSquares', style=wx.BORDER_MASK)
        self.bt1.SetFont(self.font)
        self.bt1.SetBackgroundColour('#0099FF')
        self.bt1.SetForegroundColour('White')
        self.bt2 = wx.Button(panel, -1, 'Lasso_PLS', style=wx.BORDER_MASK)
        self.bt2.SetFont(self.font)
        self.bt2.SetBackgroundColour('#FFB90F')
        self.bt2.SetForegroundColour('White')
        self.bt3 = wx.Button(panel, -1, 'Deep\nBelief\nNets', style=wx.BORDER_MASK)
        self.bt3.SetFont(self.font)
        self.bt3.SetBackgroundColour('#4EEE94')
        self.bt3.SetForegroundColour('White')
        self.bt4 = wx.Button(panel, -1, 'K-Means', style=wx.BORDER_MASK)
        self.bt4.SetFont(self.font)
        self.bt4.SetBackgroundColour('#8B6914')
        self.bt4.SetForegroundColour('White')
        self.bt5 = wx.Button(panel, -1, 'K Nearest\nNeighbor', style=wx.BORDER_MASK)
        self.bt5.SetFont(self.font)
        self.bt5.SetBackgroundColour('#9B30FF')
        self.bt5.SetForegroundColour('White')
        self.bt6 = wx.Button(panel ,-1, 'Unfinished', style=wx.BORDER_MASK)
        self.bt6.SetFont(self.font)
        self.bt6.SetBackgroundColour('#AEEEEE')
        self.bt6.SetForegroundColour('White')
        self.bt1.Bind(wx.EVT_BUTTON, self.redirect1)
        self.bt2.Bind(wx.EVT_BUTTON, self.redirect2)
        self.bt3.Bind(wx.EVT_BUTTON, self.redirect3)
        self.bt4.Bind(wx.EVT_BUTTON, self.redirect4)
        self.bt5.Bind(wx.EVT_BUTTON, self.redirect5)
        size1 = wx.BoxSizer(wx.HORIZONTAL)
        size1.Add(self.bt1, 1, wx.EXPAND)
        size1.Add(self.bt2, 1, wx.EXPAND)
        size1.Add(self.bt3, 1, wx.EXPAND)
        size2 = wx.BoxSizer(wx.HORIZONTAL)
        size2.Add(self.bt4, 1, wx.EXPAND)
        size2.Add(self.bt5, 1, wx.EXPAND)
        size2.Add(self.bt6, 1, wx.EXPAND)
        size3 = wx.BoxSizer(wx.VERTICAL)
        size3.Add(size1,1,wx.EXPAND)
        size3.Add(size2,1,wx.EXPAND)
        panel.SetSizer(size3)
        statusbar = self.CreateStatusBar()
        statusbar.SetStatusText('版权所有:计算机学院B313')

    def redirect1(self, event):
        self.Close(True)
        Second_interface.main(1)

    def redirect2(self, event):
        self.Close(True)
        Second_interface.main(2)

    def redirect3(self, event):
        self.Close(True)
        Second_interface.main(3)

    def redirect4(self, event):
        self.Close(True)
        Second_interface.main(4)

    def redirect5(self, event):
        self.Close(True)
        Second_interface.main(5)
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
