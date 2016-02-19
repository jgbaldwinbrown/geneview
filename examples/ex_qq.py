import sys

import csv
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

df = gv.util.load_dataset('GOYA_preview')
gv.gwas.qqplot(df['pvalue'], color="#00bb33", 
               xlabel="Expected p-value(-log10)", 
               ylabel="Observed p-value(-log10)")    

plt.show()
