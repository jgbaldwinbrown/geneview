import sys

import csv
import matplotlib.pyplot as plt

sys.path.append('..')  
from geneview.gwas import qqplot

pvalue=[]
with open("data/test_data.csv") as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    pvalue = [float(row[3]) for row in f_csv]

ax = qqplot(pvalue, color="#00bb33", xlabel="Expected p-value(-log10)", 
            ylabel="Observed p-value(-log10)")
plt.show()
