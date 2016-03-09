import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

x = np.random.randn(100000)
y = np.random.randn(100000) + 5
gv.hist2d(x, y)
#gv.hist2d(x, y, normed=True)
plt.show()
