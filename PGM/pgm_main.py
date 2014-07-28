# coding: utf-8

import sys, numpy as np
import PGM

def new_func(x):
    print "new function!", x

if __name__ == "__main__":
    rng = np.random.RandomState(2294322)
    n_loop_theta = 100  # thetaの増分は(1.0/n_loop_theta)．プロット点の数に対応．
    pgm = PGM.PGM(n_generate = 100000, n_y = [5, 5],  sigma = 2.0, rng = rng)
    correct_pat = pgm.i2bl(pgm.check_index)

    # 目的とするパターンが何個出てきたか
    print >> sys.stderr,  "n_appear =", pgm.n_appear

    s_index = 0

    #min_s = 1.0
    #max_s = 0.0
    #for i in range(pgm.n_generate):
    #    s = pgm.compute_S_mean(index = i)
    #    if max_s < s:
    #        max_s = s
    #    if min_s > s:
    #        min_s = s

    # すべてのパターンx[i]について，sを計算
    s = []
    for i in range(pgm.n_generate):
        #s = (pgm.compute_S_mean(index = i) - min_s)/(max_s - min_s)
        #s = rng.rand()
        #s.append((pgm.compute_S_god(index = i), i))
        s.append((pgm.compute_S_template(index = i), i))
        #s.append((pgm.compute_S_parts1(index = i, theta = 0.0), i))
        #s.append((pgm.compute_S_saccade(index = i, theta = 0.0), i))
    s = sorted(s, key = lambda x:x[0], reverse=True)

    for t in range(0, n_loop_theta + 1):
        n_FP = 0
        n_CD = 0

        theta = float(t) / n_loop_theta

        for s_index in xrange(len(s)):
            if s[s_index][0] < theta:
                break

            # x[i]をTrueだと判断した場合にCDかFPをカウント
            if pgm.x[s[s_index][1]] == correct_pat:
                n_CD += 1
            else:
                n_FP += 1

        print >> sys.stderr,  "theta =", theta
        print >> sys.stderr,  "\tn_CD =", n_CD
        print >> sys.stderr,  "\tn_FP =", n_FP

        fpr = float(n_FP)/(pgm.n_generate - pgm.n_appear)
        cdr = float(n_CD)/pgm.n_appear

        print >> sys.stderr,  "\tFPR =", fpr
        print >> sys.stderr,  "\tCDR =", cdr
        print "%lf %lf" % (fpr, cdr)
        print >> sys.stderr,  ""
