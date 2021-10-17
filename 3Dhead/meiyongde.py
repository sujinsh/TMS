from matplotlib import pyplot
import numpy as np
plt = pyplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

lmk = np.load('./data/new_lmk.npy')
# blmk = np.load('./data/blmk.npy')
# blmk /= 1000

x = lmk[:, 0].reshape(-1)
y = lmk[:, 1].reshape(-1)
z = lmk[:, 2].reshape(-1)

# 归一化
def normalizer(z):
    # max = np.max(z)
    # min = np.min(z)
    # for i in range(len(z)):
    #     z[i] = (z[i] - min) / (max - min)
    mm = np.max(z)
    for i in range(len(z)):
        if z[i] != 0:
            z[i] = -(z[i] - (mm + 100))



normalizer(z)

# xb = blmk[:, 0].reshape(-1)
# yb = blmk[:, 1].reshape(-1)
# zb = blmk[:, 2].reshape(-1)

for i in range(51):
    ax.scatter(x[i], y[i], z[i], c='r', marker='o')
    # ax.scatter(xb[i], yb[i], zb[i], c='b', marker='^')

ax.plot(x[0:5], y[0:5], z[0:5], 'g-',
        label='parametric curve')
ax.plot(x[5:10], y[5:10], z[5:10],   'g-',label='parametric curve')
ax.plot(x[10:14], y[10:14], z[10:14], 'g-',label='parametric curve')
ax.plot(x[14:19], y[14:19], z[14:19], 'g-', label='parametric curve')
ax.plot(x[19:25], y[19:25], z[19:25], 'g-',label='parametric curve')
ax.plot(x[25:31], y[25:31], z[25:31], 'g-',label='parametric curve')
ax.plot(x[31:43], y[31:43], z[31:43], 'g-',label='parametric curve')
ax.plot(x[43:], y[43:], z[43:], 'g-',label='parametric curve')


#
# ax.plot(xb[0:5],  yb[0:5], zb[0:5], 'k-',label='parametric curve')
# ax.plot(xb[5:10], yb[5:10], zb[5:10],   'k-',label='parametric curve')
# ax.plot(xb[10:14],yb[10:14], zb[10:14], 'k-',label='parametric curve')
# ax.plot(xb[14:19],yb[14:19], zb[14:19],'k-', label='parametric curve')
# ax.plot(xb[19:25],yb[19:25], zb[19:25], 'k-',label='parametric curve')
# ax.plot(xb[25:31],yb[25:31], zb[25:31], 'k-',label='parametric curve')
# ax.plot(xb[31:43],yb[31:43], zb[31:43], 'k-',label='parametric curve')
# ax.plot(xb[43:], yb[43:], zb[43:], 'k-',label='parametric curve')
# ax.legend()
plt.show()

