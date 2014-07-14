#coding: utf-8

import sys
import numpy as np

def default_p(x, sigma = 1.0, rng = None):
    if rng is None:
        print >> sys.stderr,  "warning(default_p): rng is None."
        rng = np.random
    return rng.normal(x, sigma)

class PGM(object):
    def __init__(self, 
                 n_x = 2, n_y = [3, 4], 
                 state_x = [[0, 0], [0, 1], [1, 0], [1, 1]], 
                 check_index = 3, 
                 p_x = [0.6, 0.1, 0.1, 0.2], 
                 p_y = default_p,  # 関数
                 sigma = 1.0, 
                 n_generate = 1000, rng = None):

        if rng is None:
            print >> sys.stderr,  "warning(PGM.__init__): rng is None."
            rng = np.random

        x = []
        n_appear = 0

        # ここを訂正
        for i in xrange(n_generate):
            r = rng.rand()
            for state_index in xrange(len(p_x)):
                r -= p_x[state_index]
                if r < 0.0:
                    x.append(state_x[state_index])
                    if state_index == check_index:
                        n_appear += 1
                    break

        y = []
        for i in xrange(n_generate):
            tmp_y  = []
            for j in xrange(len(n_y)):
                for k in xrange(n_y[j]):
                    tmp_y.append(p_y(x[i][j], sigma = sigma, rng = rng))
            y.append(tmp_y)

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

    def gauss(self, x, mu = 0.0, sigma = 1.0):
        return 1/(np.sqrt(2*np.pi)*self.sigma)*np.exp(-(x - mu)*(x - mu)/(2*self.sigma*self.sigma))

    def compute_S_mean(self, index = None):
        if index is None:
            print >> sys.stderr,  "warning(PGM.compute_S): index is None."
            return None
        return np.mean(self.y[index])

    def compute_S_false(self, index = None):
        if index is None:
            print >> sys.stderr,  "warning(PGM.compute_S): index is None."
            return None
        return 0.0

    def compute_S_true(self, index = None):
        if index is None:
            print >> sys.stderr,  "warning(PGM.compute_S): index is None."
            return None
        return 1.0


if __name__ == "__main__":
    rng = np.random.RandomState(2294322)
    #rng = None
    pgm = PGM(n_generate = 100000, sigma = 1.0, rng = rng)

    #for i in range(pgm.n_generate):
    #    print >> sys.stderr,  pgm.x[i]
    #    print >> sys.stderr,  pgm.y[i]

    print >> sys.stderr,  "n_appear =", pgm.n_appear
    n_loop_theta = 100
    for t in range(0, n_loop_theta + 1):
        theta = float(t) / n_loop_theta

        n_FP = 0
        n_CD = 0
        for i in range(pgm.n_generate):
            #s = pgm.compute_S_mean(index = i)
            s = rng.rand()
            if s > theta:
                z = 1
            else:
                z = 0
        
            if z == 1:
                if pgm.x[i] == pgm.state_x[pgm.check_index]:
                    n_CD += 1
                else:
                    n_FP += 1
        print >> sys.stderr,  "n_FP =", n_CD
        print >> sys.stderr,  "n_CD =", n_FP

        fpr = float(n_FP)/(pgm.n_generate - pgm.n_appear)
        cdr = float(n_CD)/pgm.n_appear

        print >> sys.stderr,  "FPR =", fpr
        print >> sys.stderr,  "CDR =", cdr

        print "%lf %lf" % (fpr, cdr)
