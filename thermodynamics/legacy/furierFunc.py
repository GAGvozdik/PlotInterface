import numpy as np
import matplotlib.pyplot as plt

class Furier:

    def __init__(self, x, y, T, n, garmNumb):
        self.x = x
        self.y = y
        self.n = n
        self.T = T
        self.garmNumb = garmNumb
        self.ak = np.zeros(int(self.n / 2))
        self.bk = np.zeros(int(self.n / 2))

    def harmA(self):

        A = np.array([(self.ak[int(k)] ** 2 + self.bk[int(k)] ** 2) ** 0.5 for k in np.linspace(0, self.T, 4)])
        return A



    def ti(self):

        dt = self.T / (self.n - 1)
        t = np.zeros(self.n)

        for i in range(self.n):
            t[i] = i * dt

        return t

    def yrmass(self):
        x = self.x
        y = self.y
        n = self.n


        print('n')
        print(n)
        print('x')
        print(x)
        print('self.garmNumb')
        print(self.garmNumb)

        garmNumb = self.garmNumb


        ak = np.zeros(int(n / 2))
        bk = np.zeros(int(n / 2))
        ck = np.zeros(int(n / 2))
        phik = np.zeros(int(n / 2))

        yr = np.zeros(n)

        # print(len(x), len(ak))

        a0 = 0
        for i in range(n):
            a0 += y[i]
        a0 *= 2 / n

        for k in range(garmNumb):
            for i in range(n):
                ak[k] += (2 / n) * (y[i] * np.cos(2 * np.pi * k * i / n))

            for i in range(n):
                bk[k] += (2 / n) * (y[i] * np.sin(2 * np.pi * k * i / n))
            ck[k] = (ak[k] ** 2 + bk[k] ** 2) ** 0.5
            # phik[k] = np.arctan(ak[k] / bk[k])

        for i in range(n):
            yr[i] = a0 / 2
            for k in range(1, garmNumb):
                yr[i] += ak[k] * np.cos(2 * np.pi * k * i / n) + bk[k] * np.sin(2 * np.pi * k * i / n)

        self.ak = ak
        self.bk = bk

        return yr

# n = 22
# t = 4
# x = np.linspace(0, t, n + 1)
# y = np.heaviside(x - 2, 1)
#
# resPoints = Furier(x, y, t, n, 13)