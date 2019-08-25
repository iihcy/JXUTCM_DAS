# coding=utf-8
# __author__=zqx


"""
将DBN提取的主成分替代pls提取的主成分(主成分分析和典型相关分析)，放到pls回归模型中
"""
from numpy import *
from sklearn import preprocessing
import sys
import time
import numpy
import os
import theano
import theano.tensor as T

from theano.tensor.shared_randomstreams import RandomStreams

from mlp import HiddenLayer
from rbm import RBM


class DBN(object):
    def __init__(self,numpy_rng, theano_rng=None, n_ins=5, hidden_layers_sizes=[4,4,4]):

        self.sigmoid_layers=[]
        self.rbm_layers=[]
        self.params=[]
        self.n_layers=len(hidden_layers_sizes)
        assert self.n_layers>0

        if not theano_rng:
            theano_rng=RandomStreams(numpy_rng.randint(123))

        self.x=T.matrix('x')

        for i in xrange(self.n_layers):
            if i==0:
                input_size=n_ins
            else:
                input_size=hidden_layers_sizes[i-1]

            if i==0:
                layer_input=self.x
            else:
                layer_input=self.sigmoid_layers[i-1].output
            sigmoid_layer=HiddenLayer(rng=numpy_rng,input=layer_input,n_in=input_size,
                                      n_out=hidden_layers_sizes[i],activation=T.nnet.sigmoid)
            self.sigmoid_layers.append(sigmoid_layer)

            self.params.extend(sigmoid_layer.params)

            rbm_layer=RBM(input=layer_input,n_visible=input_size,n_hidden=hidden_layers_sizes[i],
                          W=sigmoid_layer.W,hbias=sigmoid_layer.b,numpy_rng=numpy_rng,theano_rng=theano_rng)

            self.rbm_layers.append(rbm_layer)

    def pretraining_functions(self, x, batch_size, k):

        index=T.lscalar('index')
        learning_rate=T.scalar('lr')

        batch_begin=index*batch_size
        batch_end=batch_begin+batch_size

        pretrain_fns=[]
        last_all = []
        for rbm in self.rbm_layers:
            cost,updates,h_last=rbm.get_cost_updates(learning_rate,persistent=None,k=k)

            fn=theano.function(inputs=[index,theano.Param(learning_rate,default=0.1)],
                               outputs=cost,updates=updates,
                               givens={self.x:x[batch_begin:batch_end]})
            last = theano.function(inputs=[index, theano.Param(learning_rate, default=0.1)],
                                 outputs=h_last, updates=updates,
                                 givens={self.x: x[batch_begin:batch_end]})
            pretrain_fns.append(fn)
            last_all.append(last)
        return pretrain_fns,last_all


def loadDataSet(filename):
    fr = open(filename)
    arrayLines = fr.readlines()
    row = len(arrayLines)
    x = mat(zeros((row, 16)))
    y = mat(zeros((row, 2)))
    index = 0
    for line in arrayLines:
        curLine = line.strip().split('\t')
        x[index, :] = curLine[0:16]
        y[index, :] = curLine[16:18]
        index += 1
    e0 = preprocessing.scale(x)
    f0 = preprocessing.scale(y)
    return x, y, e0, f0


def data_Mean_Std(x0, y0):
    mean_x = mean(x0, 0)
    mean_y = mean(y0, 0)
    std_x = std(x0, axis=0, ddof=1)
    std_y = std(y0, axis=0, ddof=1)
    return mean_x, mean_y, std_x, std_y


#计算反标准化之后的系数
def Calxishu( e1, f0, row, mean_x, mean_y, std_x, std_y):
    x = numpy.hstack((e1[:, :],numpy.mat(ones((row, 1)))))
    #计算回归系数
    xishu =numpy.linalg.lstsq(x,f0)[0]
    xishu=list(xishu)
    del xishu[-1]    #删除常数项
    xishu=mat(xishu)
    m = shape(mean_x)[1]
    n = shape(mean_y)[1]
    xish = numpy.mat(numpy.zeros((m, n)))
    ch0 = numpy.mat(numpy.zeros((1, n)))
    for i in range(n):
        ch0[:, i] = mean_y[:, i] - std_y[:, i] * mean_x / std_x * xishu[:, i]
        xish[:, i] = std_y[0, i] * xishu[:, i] / std_x.T
    return ch0, xish


def test_DBN_pls(pretraining_epochs=10, pretrain_lr=0.1, k=1, batch_size=10):
    x0, y0,e0, f0= loadDataSet('data\CBM.txt')
    x0 = numpy.asarray(x0, dtype=theano.config.floatX)
    x0 = theano.shared(numpy.asarray(x0, dtype=theano.config.floatX), borrow=True)
    n_train_batches=x0.get_value(borrow=True).shape[0]/batch_size
    numpy_rng=numpy.random.RandomState(123)
    print '...building the model'

    dbn=DBN(numpy_rng,n_ins=16,hidden_layers_sizes=[10,10,8,5,5])


    print "...getting the pretraining functions"
    pretraining_fns,last_all=dbn.pretraining_functions(x=x0,batch_size=batch_size,k=k)
    print "...pretraining the model"
    start_time=time.clock()
    for i in xrange(dbn.n_layers):
        for epoch in xrange(pretraining_epochs):
            c=[]
            for batch_index in xrange(n_train_batches):
                c.append(pretraining_fns[i](index=batch_index,lr=pretrain_lr))
            print "pretraining layer %i, epoch %i,cost " %(i,epoch),
            print numpy.mean(c)
    end_time=time.clock()
    print >>sys.stderr,("The pretraining code for file "+os.path.split(__file__)[1]+" ran for %0.2fm")%((end_time-start_time)/60.)

    for i in xrange(dbn.n_layers):
        a = []
        for batch_index in xrange(n_train_batches):
            a.append(last_all[i](index=batch_index,lr=pretrain_lr))
    tran_x= numpy.array(a)
    list = []
    for line in tran_x:
        for newline in line:
            list.append(newline)
    X = mat(list)
    print X
    return X,y0,f0


def canshu(q, w, e, r):
    x, y0, f0 = test_DBN_pls(q, w, e, r)
    numpy_rng = numpy.random.RandomState(123)
    dbn = DBN(numpy_rng, n_ins=16, hidden_layers_sizes=[10,10,8,5,5])

    e1 = preprocessing.scale(x)
    e1 = mat(e1)
    mean_x, mean_y, std_x, std_y = data_Mean_Std(x, y0)

    row = shape(x)[0]
    ch0, xish = Calxishu(e1, f0, row, mean_x, mean_y, std_x, std_y)
    # 求可决系数和均方根误差
    y_predict = x * xish + tile(ch0[0, :], (row, 1))
    y_mean = tile(mean_y, (row, 1))
    SSE = sum(sum(power((y0 - y_predict), 2), 0))
    SST = sum(sum(power((y0 - y_mean), 2), 0))
    SSR = sum(sum(power((y_predict - y_mean), 2), 0))
    RR = SSR / SST
    RMSE = sqrt(SSE / row)
    return SSE, SSR, RR, RMSE, ch0, xish

if __name__ == '__main__':
    x,y0,f0=test_DBN_pls()

    e1 = preprocessing.scale(x)
    e1 = mat(e1)
    mean_x, mean_y, std_x, std_y = data_Mean_Std(x, y0)

    row = shape(x)[0]
    ch0, xish = Calxishu(e1, f0, row, mean_x, mean_y, std_x, std_y)
    # 求可决系数和均方根误差
    y_predict = x * xish + tile(ch0[0, :], (row, 1))
    y_mean = tile(mean_y, (row, 1))
    SSE = sum(sum(power((y0 - y_predict), 2), 0))
    SST = sum(sum(power((y0 - y_mean), 2), 0))
    SSR = sum(sum(power((y_predict - y_mean), 2), 0))
    RR = SSR / SST
    RMSE = sqrt(SSE / row)
    print u"可决系数:", RR
    print u"均方根误差:", RMSE
    print u"残差平方和:", SSE
    print u"回归系数："
    print ch0
    print xish