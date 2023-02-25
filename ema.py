import pandas as pd, numpy as np
import math
from collections import defaultdict


def get_df_ema(df, alpha, beta):
    emas = defaultdict(int)
    ps = defaultdict(int)
    ema_serieses = [[0 for _ in df.columns]]
    h_serieses = [[0 for _ in df.columns]]
    l_serieses = [[0 for _ in df.columns]]

    # init
    for i, p in enumerate(df.head(1).values[0]):
        emas[df.columns[i]] = p
        ema_serieses[0][i] = p

    cnt = 0
    is_first_row = True
    for r in df.iterrows():
        if is_first_row:
            is_first_row = False
            for i, p in enumerate(r[1]):
                ps[df.columns[i]] = p
            continue

        cnt += 1
        row_ema = [0 for _ in range(len(r[1]))]
        row_h = [0 for _ in range(len(r[1]))]
        row_l = [0 for _ in range(len(r[1]))]
        # for each sid (columns are sids)
        for i, p in enumerate(r[1]):
            sid = df.columns[i]
            ema = alpha * p + (1-alpha) * emas[sid]
            row_ema[i] = ema

            # depond on above
            h = (1 + beta) * ema
            l = (1 - beta) * ema
            row_h[i] = h
            row_l[i] = l
            
            #print(f'sid: {sid}, ema: {ema}, h: {h}, l: {l}, p: {p}')
            # update
            emas[df.columns[i]] = ema
            ps[df.columns[i]] = p

        ema_serieses.append(row_ema)
        h_serieses.append(row_h)
        l_serieses.append(row_l)

    df_ema = pd.DataFrame(data=ema_serieses, columns=df.columns, index=df.index)
    df_h = pd.DataFrame(data=h_serieses, columns=df.columns, index=df.index)
    df_l = pd.DataFrame(data=l_serieses, columns=df.columns, index=df.index)
    
    return df_ema, df_h, df_l
