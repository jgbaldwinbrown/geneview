import sys

import csv
import matplotlib.pyplot as plt

sys.path.append('..')  
from geneview.gwas import manhattanplot

xtick = ['1', '2','3','4','5','6','7','8','9','10','11','12','13',
         '14','16','18', '20','22']
with open("data/test_data.csv") as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    data = [[row[0], int(row[2]), float(row[3])] for row in f_csv]

ax = manhattanplot(data, xlabel="Chromosome", ylabel="-Log10(P-value)",
                   xtick_label_set = set(xtick))

plt.show()
