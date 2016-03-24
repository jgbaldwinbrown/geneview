import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

fastq = [r for r in gv.FastqReader('data/read.1.fq.gz')]
ax = gv.fqqualplot(fastq)

plt.show()
