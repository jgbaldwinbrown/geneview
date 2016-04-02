import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append('..')  
import geneview as gv

xtick = ['chr'+c for c in map(str, range(1, 15) + ['16', '18', '20', '22'])]
df = pd.read_csv('data/nifty_high.csv')
gv.gwas.manhattanplot(df[['chrID','position','pvalue']], 
                      hline_kws={'y': 3, 'color': 'b', 'lw': 1},
                      xlabel="Chromosome", 
                      ylabel="-Log10(P-value)",
                      xticklabel_kws={'rotation': 'vertical'},
                      xtick_label_set = set(xtick))
plt.savefig('nifty_hight.png')
plt.show()
