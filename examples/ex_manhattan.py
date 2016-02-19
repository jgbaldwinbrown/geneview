import sys

import csv
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

xtick = map(str, range(1, 15) + ['16','18', '20','22'])
df = gv.util.load_dataset('GOYA_preview')
gv.gwas.manhattanplot(df[['chrID','position','pvalue']], 
                      xlabel="Chromosome", 
                      ylabel="-Log10(P-value)", 
                      xtick_label_set = set(xtick))
plt.savefig('manhattan.png')
plt.show()
