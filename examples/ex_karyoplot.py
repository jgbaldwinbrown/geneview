import sys
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

fig, ax = plt.subplots(figsize=(20, 5))
gv.set_style(style='white')
gv.karyoplot('/Users/LiuSiyang/iCodeSpace/Project/geneview-data/'
             'karyotype/karyotype_human_hg19.txt', ax=ax)
plt.show()
