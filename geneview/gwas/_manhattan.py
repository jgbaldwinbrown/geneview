"""
Plotting functions for manhattan plot.

Copytright (c) Shujia Huang
Date: 2016-01-23

This model is based on brentp's script on github:
https://github.com/brentp/bio-playground/blob/master/plots/manhattan-plot.py

Thanks for Brentp's contributions

"""
from __future__ import print_function, division
from itertools import groupby, cycle
from operator import itemgetter
import functools

import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

##
from ..util import chr_id_cmp
from ..palette import color_palette

def manhattanplot(data, ax=None, xlabel=None, ylabel=None, color=None, 
                  kind='scatter', xtick_label_set=None, CHR=None, alpha=0.8, 
                  mlog10=True, hline_kws=None, xticklabel_kws=None, **kwargs):
    """Plot a manhattan plot.

    Parameters
    ----------
    data : 2d-array-like, or DataFrame.
        Input data for plot manhattan. format [[id, x_val, y_val], ...]

    ax : matplotlib axis, optional
        Axis to plot on, otherwise uses current axis.

    xlabel: string, optional
        Set the x axis label of the current axis.

    ylabel: string, optional
        Set the y axis label of the current axis.

    color : matplotlib color, optional, default: color_palette('colorful', 4) 
        Color used for the plot elements. Could hex-code or rgb, 
        e.g: '#000000,#969696' or 'rb'

    kind : {'scatter' | 'line'}, optional
        Kind of plot to draw

    xtick_label_set : a set. optional 
        Set the current x axis ticks of the current axis.

    CHR : string, or None, optional
        Choice the specific chromosome to plot. And the x-axis will be the
        position of this chromosome instead of the chromosome id.

        CAUSION: this parameter could not be used with ``xtick_label_set``
                 together.

    alpha : scalar, or 0.8(default), optional
        The alpha blending value, between 0(transparent) and 1(opaque)

    mlog10 : bool, optional, default: True
        If true, -log10 of the y_value(always be the p-value) is plotted. It
        isn't very useful to plot raw p-values, but plotting the raw value 
        could be useful for other genome-wide plots, for example peak heights,
        bayes factors, test statistics, other "scores", etc.

    hline_kws : key, value pairings, or None, optional
        keyword arguments for plotting ax.axhline

    xticklabel_kws : key, value pairings, or None, optional
        Other keyword arguments are passed to set_xticklabels in 
        maplotlib.axis.Axes.set_xticklabels.

    kwargs : key, value pairings, optional
        Other keyword arguments are passed to ``plt.scatter()`` or
        ``plt.vlines()`` (in matplotlib.pyplot) depending on whether 
        a scatter or line plot is being drawn.


    Returns
    -------
    ax : matplotlib Axes
        Axes object with the manhattanplot.


    Notes
    -----
    1. This plot function is not just suit for GWAS manhattan plot,
       it could also be used for any input data which format is ::

        [ [id1, x-value1, y-value1],
          [id2, x-value2, y-value2],
          ...
        ]

    2. The right and top spines of the plot have been setted to be 
       invisible by default.

    3. I'm going to add a parameter calls ``highlight`` to highlight a
       set of interesting positions (SNPs). And this parameter takes a 
       list-like value.

    Examples
    --------

    Plot a basic manhattan plot:

    .. plot::
        :context: close-figs

        >>> import geneview as gv
        >>> df = gv.util.load_dataset('GOYA_preview')
        >>> gv.gwas.manhattanplot(df[['chrID','position','pvalue']],
        ...                       xlabel="Chromosome", 
        ...                       ylabel="-Log10(P-value)") 

    Plot a basic manhattan plot with vertical xtick labels:

    .. plot::
        :context: close-figs

        >>> xtick = ['chr'+c for c in 
        ...          map(str, range(1, 15) + ['16', '18', '20', '22'])]
        >>> gv.gwas.manhattanplot(df[['chrID','position','pvalue']],  
        ...                       xlabel="Chromosome", 
        ...                       ylabel="-Log10(P-value)", 
        ...                       xticklabel_kws={'rotation': 'vertical'},
        ...                       xtick_label_set = set(xtick))

    Add a horizotal at y position=3 line with blue color and lingwidth=1 
    across the axis:

    .. plot::
        :context: close-figs
    
        >>> gv.gwas.manhattanplot(df[['chrID','position','pvalue']],  
        ...                       hline_kws={'y': 3, 'color': 'b', 'lw': 1},
        ...                       xlabel="Chromosome", 
        ...                       ylabel="-Log10(P-value)", 
        ...                       xticklabel_kws={'rotation': 'vertical'},
        ...                       xtick_label_set = set(xtick))

    """
    if CHR is not None and xtick_label_set is not None:
        msg = "``CHR`` and ``xtick_label_set`` can't be setted simultaneously."
        raise ValueError(msg)

    # Draw the plot and return the Axes
    if ax is None:
        ax = plt.gca()

    if xticklabel_kws is None:
        xticklabel_kws = dict()
    if hline_kws is None:
        hline_kws = dict()

    # Get the color from 'colorful' cycle
    if color is None:
        color = color_palette("colorful", 4) 

    if ',' in color: color = color.split(',')
    colors = cycle(color)

    if isinstance(data, DataFrame):
        data = DataFrame(data.values, columns=['chrom', 'pos', 'pvalue'])
    else:
        data = DataFrame(data, columns=['chrom', 'pos', 'pvalue'])

    last_x = 0
    xs_by_id = {} # use for collecting chromosome's position on x-axis
    x, y, c = [], [], []
    for seqid, rlist in data.groupby('chrom', sort=False):

        if CHR is not None and seqid != CHR: continue
        
        color = next(colors)
        region_xs = [last_x + r for r in rlist['pos']]
        x.extend(region_xs)
        y.extend(rlist['pvalue'])
        c.extend([color] * len(rlist))

        # ``xs_by_id`` is for setting up positions and ticks. Ticks should
        # be placed in the middle of a chromosome. The a new pos column is 
        # added that keeps a running sum of the positions of each successive 
        # chromsome.
        xs_by_id[seqid] = (region_xs[0] + region_xs[-1]) / 2
        last_x = x[-1]  # keep track so that chrs don't overlap in the plot.

    if not x:
        msg = ("zero-size array to reduction operation minimum which has no "
               "identity. This could be caused by zero-size array of ``x`` "
               "in the ``manhattanplot(...)`` function.")
        raise ValueError(msg)

    c = np.array(c)
    x = np.array(x)
    y = -np.log10(y) if mlog10 else np.array(y)

    if kind == 'scatter':
        ax.scatter(x, y, c=c, alpha=alpha, edgecolors='none', **kwargs)

    elif kind == 'line':
        ax.vlines(x, 0, y, colors=c, alpha=alpha, **kwargs)

    else:
        msg = "``kind`` must be either 'scatter' or 'line'"
        raise ValueError(msg)

    if hline_kws:
        ax.axhline(**hline_kws)

    if xtick_label_set is None: 
        xtick_label_set = set(xs_by_id.keys())

    if CHR is None:
        xs_by_id = [(k, xs_by_id[k])
                     for k in sorted(xs_by_id.keys(), key=functools.cmp_to_key(chr_id_cmp))
                     if k in xtick_label_set]

        ax.set_xticks([c[1] for c in xs_by_id])
        ax.set_xticklabels([c[0] for c in xs_by_id], **xticklabel_kws)

    else:
        # show the whole chromsome's position without scientific notation
        # if you are just interesting in this chromosome.
        ax.get_xaxis().get_major_formatter().set_scientific(False)

    ax.set_xlim(0, x[-1])
    ax.set_ylim(ymin=y.min())

    if xlabel: ax.set_xlabel(xlabel) 
    if ylabel: ax.set_ylabel(ylabel)

    return ax
