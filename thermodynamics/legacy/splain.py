import numpy as np

def progon(a1, b1, c1, d1, n):

    a = np.copy(a1)
    b = np.copy(b1)
    c = np.copy(c1)
    d = np.copy(d1)

    polC = np.zeros(n)

    alpha = np.zeros(n)
    beta = np.zeros(n)

    for i in range(1, n - 1):
        z = (a[i] * alpha[i - 1] + c[i])
        alpha[i] = -b[i] / z
        beta[i] = (d[i] - a[i] * beta[i - 1]) / z

    for i in range(n - 2, 0, -1):
        polC[i] = alpha[i] * polC[i + 1] + beta[i]

    return polC


def mySpline(x, y, n):
    a = np.copy(y)
    b = np.zeros(n)
    c = np.zeros(n)
    d = np.zeros(n)
    h = np.zeros(n)

    for i in range(n - 1):
        h[i] = x[i + 1] - x[i]

    for i in range(1, n - 1):
        a[i] = h[i - 1]
        b[i] = h[i]
        c[i] = 2.0 * (h[i - 1] + h[i])
        d[i] = 6.0 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

    polA = np.copy(y)
    polB = np.zeros(n)
    polC = progon(a, b, c, d, n)
    polD = np.zeros(n)

    for i in range(n - 1, 0, -1):
        h[i - 1] = x[i] - x[i - 1]
        polD[i] = (polC[i] - polC[i - 1]) / h[i - 1]
        polB[i] = h[i - 1] * (2.0 * polC[i] + polC[i - 1]) / 6.0 + (y[i] - y[i - 1]) / h[i - 1]

    return polA, polB, polC, polD




























