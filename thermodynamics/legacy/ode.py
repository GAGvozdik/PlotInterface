import matplotlib.pyplot as plt
import numpy as np

n = 22
a = 0
b = 2

x = np.linspace(a, b, n)

yn = - (1 / (x - 1))
# yn = 1 / 4 * (x + 2) ** 2
# yn = 2 * np.e ** x

y = np.zeros(n)
y[0] = 1

def func(x, y):
    return y ** 2


fig = plt.figure()


# ax1 = fig.add_subplot()
plt.ylim (-10, 10)

plt.plot(x, yn, c='orange')
plt.scatter(x, yn, c='orange', s=9)

h = x[1] - x[0]

for i in range(n - 1):

    k1 = h * func(x[i], y[i])
    k2 = h * func(x[i] + h / 2, y[i] + k1 / 2)
    k3 = h * func(x[i] + h / 2, y[i] + k2 / 2)
    k4 = h * func(x[i] + h, y[i] + k3)

    y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    # if x[i] > 20:
    #     y[i] = 0

plt.scatter(x, y, c='blue', s=7)
plt.plot(x, y, c='blue')

plt.show()















