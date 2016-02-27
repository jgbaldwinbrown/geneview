import sys
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

df = gv.util.load_dataset('GOYA_preview')
gv.gwas.qqplot(df['pvalue']) 
"""
fig, ax = plt.subplots()
gv.gwas.qqplot(df['pvalue'], ax=ax,
               xlabel="Expected p-value(-log10)", 
               ylabel="Observed p-value(-log10)")
"""
plt.savefig('qq.png')
plt.show()
