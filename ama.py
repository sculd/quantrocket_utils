import pandas as pd, numpy as np
import math
from collections import defaultdict


def get_df_ama(df, alpha_min, alpha_max, beta, gamma):
    alphas = defaultdict(int)
    amas = defaultdict(int)
    dposs = defaultdict(int)
    dnegs = defaultdict(int)
    ps = defaultdict(int)
    ama_serieses = [[0 for _ in df.columns]]
    h_serieses = [[0 for _ in df.columns]]
    l_serieses = [[0 for _ in df.columns]]

    # init
    for i, p in enumerate(df.head(1).values[0]):
        amas[df.columns[i]] = p
        ama_serieses[0][i] = p
        alphas[df.columns[i]] = alpha_min

    cnt = 0
    is_first_row = True
    for r in df.iterrows():
        if is_first_row:
            is_first_row = False
            for i, p in enumerate(r[1]):
                ps[df.columns[i]] = p
            continue

        cnt += 1
        row_ama = [0 for _ in range(len(r[1]))]
        row_h = [0 for _ in range(len(r[1]))]
        row_l = [0 for _ in range(len(r[1]))]
        # for each sid (columns are sids)
        for i, p in enumerate(r[1]):
            sid = df.columns[i]
            ama = alphas[sid] * p + (1-alphas[sid]) * amas[sid]
            row_ama[i] = ama
            change = (p - ps[sid]) / ps[sid]
            dpos = alphas[sid] * max(change, 0) + (1-alphas[sid]) * dposs[sid]
            dneg = -alphas[sid] * min(change, 0) + (1-alphas[sid]) * dnegs[sid]

            # depond on above
            h = (1 + beta * dnegs[sid]) * ama
            l = (1 - beta * dposs[sid]) * ama
            row_h[i] = h
            row_l[i] = l
            pa = (p - amas[sid]) / amas[sid]
            if p > h:
                s = (beta * dpos)
                if s == 0:
                    snr = 0
                else:
                    snr = pa / s
            elif p < l:
                s = (beta * dneg)
                if s == 0:
                    snr = 0
                else:
                    snr = -pa / s
            else:
                snr = 0

            # depend on above
            alpha = alpha_min + (alpha_max - alpha_min) * math.atan(gamma * snr) / (math.pi / 2)

            #print(f'sid: {sid}, ama: {ama}, dpos: {dpos}, dneg: {dneg}, alpha: {alpha}, h: {h}, l: {l}, snr: {snr}, p: {p}, change: {change}')
            # update
            amas[df.columns[i]] = ama
            dposs[df.columns[i]] = dpos
            dnegs[df.columns[i]] = dneg
            alphas[df.columns[i]] = alpha
            ps[df.columns[i]] = p

        ama_serieses.append(row_ama)
        h_serieses.append(row_h)
        l_serieses.append(row_l)

    df_ama = pd.DataFrame(data=ama_serieses, columns=df.columns, index=df.index)
    df_h = pd.DataFrame(data=h_serieses, columns=df.columns, index=df.index)
    df_l = pd.DataFrame(data=l_serieses, columns=df.columns, index=df.index)
    
    return df_ama, df_h, df_l