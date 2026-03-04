import matplotlib.pyplot as plt
import numpy as np



fig, ax = plt.subplots(1, 1, figsize=(8, 6))

n = 100

def get_coords(xc, yc, alpha):
    
    return None

x = np.random.rand(n) * 2
y = np.random.rand(n) * 2

ax.scatter(x, y, color='Crimson')


x = np.random.rand(n) * 2 + 2
y = np.random.rand(n) * 2
ax.scatter(x, y, color='darkcyan')

x = np.random.rand(n) * 2 + 1
y = np.random.rand(n) * 2 + 2
ax.scatter(x, y, color='orange')

plt.show()