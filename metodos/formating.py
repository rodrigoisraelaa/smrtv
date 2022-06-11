import numpy as np
import math

from datetime import datetime


def formatingpausas(x):
    x = x.values
    x = x[5:, :]
    y = np.append(np.append(x[:29, :7], x[:29, 7:14]), x[:15, 14:21])
    y = np.reshape(y, (73, 7))
    y = np.delete(y, 1, axis=1)
    return y


def formatingprogram(x):
    x = x.values
    x = x[4:]
    y = []
    for t in x[:, 0]:
        h = t.strftime("%H:%M")
        u = (float(h[:2])+float(h[-2:])/60)/24
        y.append(u)
    x[:, 0] = y
    return x
