import numpy as np
import matplotlib.pyplot as plt

import geneview as gv

x_mu, x_sigma = 0, 0.1 # mean and standard deviation
y_mu, y_sigma = 10, 0.3 # mean and standard deviation

x = np.random.normal(x_mu, x_sigma, 1000)
y = np.random.normal(y_mu, y_sigma, 1000)

g = gv.jointplot(x=x, y=y, kind="hex")
plt.savefig('hex.pdf')
#plt.show()
