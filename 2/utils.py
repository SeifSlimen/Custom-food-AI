#coding: utf8
import pandas as pd
import numpy as np

def sublist_uniques(data,sublist):
    categories = set()
    for d, t in data.iterrows():
        try:
            for j in t[sublist]:
                categories.add(j)
        except Exception as e:
            # Optionally log or print(e)
            pass
    return list(categories)

def sublists_to_binaries(data, sublist, index_key=None):
    categories = sublist_uniques(data, sublist)
    frame = pd.DataFrame(columns=categories)
    for d, i in data.iterrows():
        if isinstance(i[sublist], (list, np.ndarray)):
            try:
                if index_key is not None:
                    key = i[index_key]
                    f = np.zeros(len(categories))
                    for j in i[sublist]:
                        if j in categories:
                            f[categories.index(j)] = 1
                    if key in frame.index:
                        for j in i[sublist]:
                            if j in categories:
                                frame.at[key, j] += 1
                    else:
                        frame.loc[key] = f
                else:
                    f = np.zeros(len(categories))
                    for j in i[sublist]:
                        if j in categories:
                            f[categories.index(j)] = 1
                    frame.loc[d] = f
            except Exception as e:
                # Optionally log or print(e)
                pass
    return frame