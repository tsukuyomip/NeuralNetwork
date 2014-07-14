# coding: utf-8

import sys, numpy as np
import PGM

if __name__ == "__main__":
    rng = np.random.RandomState(2294322)
    n_loop_theta = 100  # thetaの増分は(1.0/n_loop_theta)．プロット点の数に対応．
    pgm = PGM.PGM(n_generate = 100000, sigma = 1.0, rng = rng)

    # 目的とするパターンが何個出てきたか
    print >> sys.stderr,  "n_appear =", pgm.n_appear


    for t in range(0, n_loop_theta + 1):
        theta = float(t) / n_loop_theta

        n_FP = 0
        n_CD = 0

        min_s = 1.0
        max_s = 0.0
        for i in range(pgm.n_generate):
            s = pgm.compute_S_mean(index = i)
            if max_s < s:
                max_s = s
            if min_s > s:
                min_s = s

        # すべてのパターンx[i]について，sを計算
        for i in range(pgm.n_generate):
            s = (pgm.compute_S_mean(index = i) - min_s)/(max_s - min_s)
            #s = rng.rand()
            #s = pgm.compute_S_god(index = i)
            if s > theta:
                z = 1
            else:
                z = 0

            # x[i]をTrueだと判断した場合にCDかFPをカウント
            if z == 1:
                if pgm.x[i] == pgm.state_x[pgm.check_index]:
                    n_CD += 1
                else:
                    n_FP += 1

        print >> sys.stderr,  "theta =", theta
        print >> sys.stderr,  "\tn_FP =", n_CD
        print >> sys.stderr,  "\tn_CD =", n_FP

        fpr = float(n_FP)/(pgm.n_generate - pgm.n_appear)
        cdr = float(n_CD)/pgm.n_appear

        print >> sys.stderr,  "\tFPR =", fpr
        print >> sys.stderr,  "\tCDR =", cdr
        print "%lf %lf" % (fpr, cdr)
        print >> sys.stderr,  ""
