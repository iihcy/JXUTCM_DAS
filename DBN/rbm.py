# coding=utf-8
# __author__=zqx

import numpy
import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams


class RBM(object):
    def __init__(self,input=None,n_visible=None,n_hidden=None,\
                 W=None,hbias=None,vbias=None,numpy_rng=None,
                 theano_rng=None):

        self.n_visible=n_visible
        self.n_hidden=n_hidden

        #生成随机数
        if numpy_rng is None:
            numpy_rng=numpy.random.RandomState(1234)

        if theano_rng is None:
            theano_rng=RandomStreams(numpy_rng.randint(2**30))

        if W is None:
            initial_W=numpy.asarray(numpy_rng.uniform(
                    low=-4*numpy.sqrt(6./(n_hidden+n_visible)),
                    high=4*numpy.sqrt(6./(n_hidden+n_visible)),
                    size=(n_visible,n_hidden)),
                    dtype=theano.config.floatX)
            W=theano.shared(value=initial_W,name='W',borrow=True)

        if hbias is None:
            hbias=theano.shared(value=numpy.zeros(n_hidden,
                                                  dtype=theano.config.floatX),
                                name='hbias',borrow=True)
        if vbias is None:
            vbias=theano.shared(value=numpy.zeros(n_visible,
                                                  dtype=theano.config.floatX),
                                name='vbias',borrow=True)
        self.input=input
        if not input:
            self.input=T.matrix('input')

        self.W=W
        self.hbias=hbias
        self.vbias=vbias
        self.theano_rng=theano_rng

        self.params=[self.W,self.hbias,self.vbias]

    #计算自由能
    def free_energy(self,v_sample):
        wx_b=T.dot(v_sample,self.W)+self.hbias
        vbias_term=T.dot(v_sample,self.vbias)
        hbias_term=T.sum(T.log(1+T.exp(wx_b)),axis=1)
        return -vbias_term-hbias_term

    #定义向上传播
    def propup(self,vis):
        pre_sigmoid_activation=T.dot(vis,self.W)+self.hbias
        return [pre_sigmoid_activation,T.nnet.sigmoid(pre_sigmoid_activation)]

    #给定v单元计算h单元的函数
    def sample_h_given_v(self,v0_sample):
        pre_sigmoid_h1,h1_mean=self.propup(v0_sample)
        h1_sample=self.theano_rng.binomial(size=h1_mean.shape,
                                           n=1,p=h1_mean,
                                           dtype=theano.config.floatX)
        return [pre_sigmoid_h1,h1_mean,h1_sample]

    #定义向下传播
    def propdown(self,hid):
        pre_sigmoid_activation=T.dot(hid,self.W.T)+self.vbias
        return [pre_sigmoid_activation,T.nnet.sigmoid(pre_sigmoid_activation)]


    #给定h单元计算v单元的函数
    def sample_v_given_h(self,h0_sample):

        pre_sigmoid_v1,v1_mean=self.propdown(h0_sample)
        v1_sample=self.theano_rng.binomial(size=v1_mean.shape,n=1,p=v1_mean,
                                           dtype=theano.config.floatX)
        return [pre_sigmoid_v1,v1_mean,v1_sample]

    #从隐藏状态出发，执行一步Gibbs采样过程
    def gibbs_hvh(self,h0_sample):

        pre_sigmoid_v1,v1_mean,v1_sample=self.sample_v_given_h(h0_sample)
        pre_sigmoid_h1,h1_mean,h1_sample=self.sample_h_given_v(v1_sample)
        return [pre_sigmoid_v1,v1_mean,v1_sample,
                pre_sigmoid_h1,h1_mean,h1_sample]

    #从可见状态出发，执行一步Gibbs采样过程
    def gibbs_vhv(self,v0_sample):
        pre_sigmoid_h1,h1_mean,h1_sample=self.sample_h_given_v(v0_sample)
        pre_sigmoid_v1,v1_mean,v1_sample=self.sample_v_given_h(h1_sample)
        return [pre_sigmoid_h1,h1_mean,h1_sample,
                pre_sigmoid_v1,v1_mean,v1_sample]

    def get_cost_updates(self,lr=0.1,persistent=None,k=1):


        #计算正项
        pre_sigmoid_ph,ph_mean,ph_sample=self.sample_h_given_v(self.input)
        #决定初始化固定链的方法:对于CD，采用全新生成隐含样本；对于PCD，从链的旧状态获得
        if persistent is None:
            chain_start=ph_sample
        else:
            chain_start=persistent

        [pre_sigmoid_nvs,nv_means,nv_samples,
         pre_sigmoid_nhs,nh_means,nh_samples],updates=\
            theano.scan(self.gibbs_hvh,
                    #下面字典中前5项为None,表示chain_start与初始状态中第六个输出量有关
                    outputs_info=[None,None,None,None,None,chain_start],
                    n_steps=k)
        #计算RBM参数的梯度,只需要从链末端采样
        chain_end=nv_samples[-1]

        cost=T.mean(self.free_energy(self.input))-T.mean(self.free_energy(chain_end))
        #因为chai_end是符号变量，而我们只根据链最末端的数据求梯度，所有指定chain_end为常数
        gparams=T.grad(cost,self.params,consider_constant=[chain_end])

        #构造更新字典
        for gparam,param in zip(gparams,self.params):
            #确保学习率lr的数据类型正确
            updates[param]=param-gparam*T.cast(lr,dtype=theano.config.floatX)

        #RBM是深度网络的一个模块时,更新perisistent
        if persistent:
            #只有persistent为共享变量时才运行
            updates[persistent]=nh_samples[-1]
            #伪似然函数是PCD的一个较好的代价函数
            monitoring_cost=self.get_pseudo_likehood_cost(updates)
        #RBM是标准网络
        else:
            #重构交叉熵是CD的一个较好的代价函数
            monitoring_cost=self.get_reconstruction_cost(updates,pre_sigmoid_nvs[-1])

        h = T.nnet.sigmoid(T.dot(self.input, self.W) + self.hbias)
        reconstructed_v = T.nnet.sigmoid(T.dot(h, self.W.T) + self.vbias)
        h_last = T.nnet.sigmoid(T.dot(reconstructed_v, self.W) + self.hbias)

        return monitoring_cost,updates,h_last

    def get_reconstruction_cost(self,updates,pre_sigmoid_nv):

        cross_entropy=T.mean(T.sum(self.input*T.log(T.nnet.sigmoid(pre_sigmoid_nv))+
                                   (1-self.input)*T.log(1-T.nnet.sigmoid(pre_sigmoid_nv)),axis=1))
        return cross_entropy