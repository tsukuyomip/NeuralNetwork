#coding: utf-8

import sys
import numpy as np

class PGM(object):
    def __init__(self, 
                 n_x = 2, n_y = [3, 4], 
                 state_x = [[0, 0], [0, 1], [1, 0], [1, 1]], 
                 check_index = 3, 
                 p_x = [0.6, 0.1, 0.1, 0.2], 
                 p_y = None,
                 sigma = 1.0, 
                 n_generate = 1000, rng = None):
        p_y = self.y_gen_normal

        if rng is None:
            print >> sys.stderr,  "warning(PGM.__init__): rng is None."
            rng = np.random

        # パターンを n_generate 個生成．
        (x, n_appear) = self.generate_x(n_generate, p_x, state_x, check_index, rng)

        # 各x[i]に対してy[i][j]を生成
        y = self.generate_y(n_generate, n_y, p_y, x, sigma, rng)

        self.n_x = n_x
        self.n_y = n_y
        self.state_x = state_x
        self.check_index = check_index
        self.p_x = p_x
        self.p_y =p_y
        self.sigma = sigma
        self.n_generate = n_generate

        self.x = x
        self.y = y
        self.n_appear = n_appear


    def generate_x(self, n_generate, p_x, state_x, check_index, rng):
        x = []
        n_appear = 0

        for i in xrange(n_generate):
            r = rng.rand()
            for state_index in xrange(len(p_x)):
                r -= p_x[state_index]
                if r < 0.0:
                    x.append(state_x[state_index])
                    if state_index == check_index:
                        n_appear += 1
                    break

        #self.x = x  # __init__()でselfに代入．
        #self.n_appear = n_appear  # __init__()で．
        return (x, n_appear)

    def generate_y(self, n_generate, n_y, p_y, x, sigma, rng):
        y = []
        for i in xrange(n_generate):
            tmp_y  = []
            for j in xrange(len(n_y)):
                for k in xrange(n_y[j]):
                    tmp_y.append(p_y(x = x[i][j], sigma = sigma, rng = rng))
            y.append(tmp_y)

        #self.y = y  # __init__()で．
        return y

    def y_gen_normal(self, x = 0.0, sigma = 1.0, rng = None):
        """xをもとにyの値をひとつ生成する．（平均x 分散sigma の正規分布）"""
        if rng is None:
            print >> sys.stderr,  "warning(PGM.y_gen_normal): rng is None. set 'rng' to 'np.random'"
            rng = np.random
        return rng.normal(x, sigma)

    def gauss(self, x, mu = 0.0, sigma = 1.0):
        """gauss関数の値を返す．
        今回は確率密度関数p(y|x)の値を取得する際に使用．"""
        return 1/(np.sqrt(2*np.pi)*self.sigma)*np.exp(-(x - mu)*(x - mu)/(2*self.sigma*self.sigma))

    def compute_S_mean(self, index = None):
        """y[index]の平均を返す．"""
        if index is None:
            print >> sys.stderr,  "warning(PGM.compute_S): index is None."
            return None
        return np.mean(self.y[index])

    def compute_S_false(self, index = None):
        """常にFalse（0.0）を返す"""
        if index is None:
            print >> sys.stderr,  "warning(PGM.compute_S): index is None."
            return None
        return 0.0

    def compute_S_true(self, index = None):
        """常にTrue（1.0）を返す"""
        if index is None:
            print >> sys.stderr,  "warning(PGM.compute_S): index is None."
            return None
        return 1.0

    def compute_S_god(self, index = None):
        """課題6のh_G()により，Sを計算"""

        h = 0.0
        for i in xrange(len(self.state_x)):
            x = self.state_x[i]
            tmpsum = 0.0
            for j in xrange(self.n_x):
                for k in xrange(sum(self.n_y)):
                    tmpsum += (1.0 - 2*self.y[index][k] + 2*self.y[index][k]*x[j] - x[j]*x[j])
            tmpsum = tmpsum/(2.0*self.sigma*self.sigma)

            h += self.p_x[i]*np.exp(tmpsum)/self.p_x[self.check_index]
        return 1.0/h

    def compute_S_template(self, index = None):
        """課題7のh_T()により，Sを計算．"""
        tmpsum = 0.0
        for i in xrange(sum(self.n_y)):
            tmpsum += 1.0 - 2*self.y[index][i]
        tmpsum = tmpsum/(2.0*self.sigma*self.sigma)
        h = 1.0 + (self.p_x[0]/self.p_x[3])*np.exp(tmpsum)
        return 1.0/h

