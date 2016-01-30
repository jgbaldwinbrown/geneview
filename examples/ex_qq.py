"""
    Copytright (c) Shujia Huang
    Date: 2016-01-23

    Plot a Q-Q plot of the input file(s).
    python %prog [options] files
"""

import optparse
import sys
from itertools import groupby, cycle
from operator import itemgetter
from matplotlib import pyplot as plt
import numpy as np

sys.path.append('..')
from geneview.gwas import qqplot


def _gen_data(fhs, columns, sep):
    """
    iterate over the files and yield: pvalue
    """
    for fh in fhs:
        for line in fh:
            if line[0] == '#': continue
            toks = line.strip('\n').split(sep) if sep else line.strip('\n').split()
            yield float(toks[columns[2]])

def qq(fhs, columns, sep, no_log, image_path, title, color, 
       xlabel, ylabel, ymax):

    data = [d for d in _gen_data(fhs, columns, sep)]

    # Plotting the qq image
    plt.close() # in case plot accident
    #f, ax = plt.subplots(ncols=1, nrows=1, figsize=(14, 8), tight_layout=True)
    f, ax = plt.subplots(ncols=1, nrows=1, tight_layout=True)
    ax = qqplot(data, color=color, mlog10=not no_log)
    if ymax is not None: ax.set_ylim(ymax=ymax)

    if title:
        ax.set_title(title, loc='center', fontsize=18)

    ax.tick_params(labelsize=14)
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)

    print >> sys.stderr, 'saving to: %s' % image_path
    plt.savefig(image_path)
    plt.show()
    

def get_filehandles(args):
    return (open(a) if a != "-" else sys.stdin for a in args)

def main():
    COLORFUL = '#6DC066,#FD482F,#8A2BE2,#3399FF'
    p = optparse.OptionParser(__doc__)
    p.add_option("--no-log", dest="no_log", help="don't do -log10(p) on the value",
                 action='store_true', default=False)
    p.add_option("--cols", dest="cols", help="zero-based column indexes to get "
                 "chr, position, p-value respectively e.g. %default", 
                 default="0,1,2")
    p.add_option("--sep", help="data separator, default is any space",
                 default=None, dest="sep")
    p.add_option("--color", dest="color", help="the dots color",
                 default="#969696")
    p.add_option("--image", dest="image", 
                 help="save the image_path to this file. e.g. %default",
                 default="qq.png")
    p.add_option("--title", help="title for the image.", default=None, 
                 dest="title")
    p.add_option("--xlabel", help="The xlabel.", 
                 default="Expected p-value(-log10)", 
                 dest="xlabel")
    p.add_option("--ylabel", help="The ylabel.", 
                 default="Observed p-value(-log10)", 
                 dest="ylabel")
    p.add_option("--ymax", help="max (logged) y-value for plot", dest="ymax", 
                 type='float')

    opts, args = p.parse_args()
    if (len(args) == 0):
        sys.exit(not p.print_help())

    fhs = get_filehandles(args)
    columns = map(int, opts.cols.split(","))
    qq(fhs, columns, opts.sep, opts.no_log, opts.image, opts.title, 
       opts.color, opts.xlabel, opts.ylabel, opts.ymax)

if __name__ == "__main__":
    main()
