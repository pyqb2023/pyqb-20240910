# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Programming in Python
# ## Exam: September 10, 2024
#
# You can solve the exercises below by using standard Python 3.11 libraries, NumPy, Matplotlib, Pandas, PyMC.
# You can browse the documentation: [Python](https://docs.python.org/3.11/), [NumPy](https://numpy.org/doc/1.26/index.html), [Matplotlib](https://matplotlib.org/3.8.2/users/index.html), [Pandas](https://pandas.pydata.org/pandas-docs/version/2.1/index.html), [PyMC](https://www.pymc.io/projects/docs/en/v5.10.3/api.html).
# You can also look at the slides or your code on [GitHub](https://github.com).
#
# **It is forbidden to communicate with others or "ask questions" online (i.e., stackoverflow is ok if the answer is already there, but you cannot ask a new question or use ChatGPT or similar products)**
#
# To test examples in docstrings use
#
# ```python
# import doctest
# doctest.testmod()
# ```
#

import numpy as np
import pandas as pd             # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pymc as pm               # type: ignore
import arviz as az              # type: ignore

# ### Exercise 1 (max 2 points)
#
# You have to analyze the genome of *Seicercus examinandus* as collected by the US National Center for Biotechnology Information (NCBI Reference Sequence: NC_051526.1). You have the data in FASTA format: a text file in which the first line (starting with >) is a comment (and should be ignored), then you get the genome data split over many lines. The file is [nc_051526_1.fasta](nc_051526_1.fasta).
#
# Read the genome in a variable of type `str`.

# +
genome = ''

with open('nc_051526_1.fasta') as f_genome:
    for line in f_genome:
        if not line.startswith('>'):
            genome += line.strip()
# -

# ### Exercise 2 (max 5 points)
#
# Consider the **set** of the letters appearing in the genome string. Compute all the triplets that can be composed by using these letters (for example: `'AAC'`), by considering each and its reverse only once: for example, only one between `'AAC'` and `'CAA'` should appear in the result. Name the result `possible_triplets`.

letters = frozenset(genome)
possible_triplets = set()
for a in letters:
    for b in letters:
        for c in letters:
            triplet = a+b+c
            if triplet[::-1] not in possible_triplets: 
                possible_triplets.add(triplet)
possible_triplets, len(possible_triplets)

# +
from itertools import combinations_with_replacement

set([''.join(c) for c in combinations_with_replacement("ACGT", 3)])


# -

# ### Exercise 3 (max 7 points)
#
# Define a function which takes a string of arbitrary length ($\ge 3$) and a triplet, and returns the number of occurrences of the triplet or its reverse in the string. For example the triplet `'AAT'` occurs three times (twice as `'AAT'` and once as `'TAA'`) in `'CAATAATCC'` and the triplet `'AAA'` occurs five times in `'AAAAAAA'`.
#
# To get the full marks, you should declare correctly the type hints (the signature of the function) and add a doctest string.

def num_triplets(s: str, triplet: str) -> int:
    """Return the number of times triplet or its reverse occurs in s.
    
    >>> num_triplets('CAATAATCC', 'AAT')
    3
    >>> num_triplets('CAATAATCC', 'TAA')
    3
    >>> num_triplets('AAAAAAA', 'AAA')
    5
    """
    assert len(s) >= 3 and len(triplet) == 3
    
    rev_triplet = triplet[-1::-1]
    res = 0
    for i in range(0, len(s)-2):
        if s[i:i+3] == triplet or s[i:i+3] == rev_triplet:
            res = res + 1
    return res


import doctest
doctest.testmod()


# ### Exercise 4 (max 5 points)
#
# Define a pandas DataFrame indexed by the possible triplets identified in Exercise 2, with a column reporting the occurrences of each triplet in the genome under analysis. For example, the triplet `'AGG'` should have 356 occurrences. Add a column `even`, with a value of `True` if the number of occurrences is even and `False` otherwise.

df = pd.DataFrame(index=list(possible_triplets), columns=['num'])
df['num'] = df.index.map(lambda x: num_triplets(genome, x))
df['even'] = df['num'].map(lambda x: x % 2 == 0)

# ### Exercise 5 (max 2 points)
#
# Add a column with the "standardized number of occurrences" `std_num` of each triplet. The *standardized number of occurrences* is defined as the difference between a value and the mean over all the values, divided by the standard deviation over all the values. 

df['std_num'] = (df['num'] - df['num'].mean()) / df['num'].std()

df

# ### Exercise 6 (max 3 points)
#
# Plot a histogram of the values `std_num` using a list `[-3, -2.5, -2, ..., 2, 2.5, 3]` to define the 12 bins. Add to the figure also a red dashed vertical line marking the mean.
#

fig, ax = plt.subplots()
ax.vlines(df['std_num'].mean(), 0, .6, 'red', linestyle='--')
_ = ax.hist(df['std_num'], bins=[-3 + x*.5 for x in range(13)], density=True)


# ### Exercise 7 (max 5 points)
#
#
# Plot two histograms (two different plots on one horizontal row, add also a legend to the figure), one for the triplets occuring an even number of times, one for the others. The two histograms should depict the values in increasing order.

# +
even = df.query('even == True')['num'].sort_values()
odd = df.query('even == False')['num'].sort_values()

fig, ax = plt.subplots(ncols=2)
ax[0].bar(even.index, even, label='Even', color='blue')
ax[1].bar(odd.index, odd, label='Odd', color='red')
_ = fig.legend()

# -

# ### Exercise 8 (max 4 points)
#
# Consider this statistical model: the *standardized number of occurrences* of even and not even triplets is normally distributed, with an unknown mean, and an unknown standard deviation. Your *a priori* estimation of the mean is given by a normal distribution with mean 0 and standard deviation 2; your prior estimation for the standard deviation is an exponential distribution with $\lambda = 1$. Use PyMC to sample the posterior distributions after having seen the actual values for even and not even triplets.  Plot the posterior.

with pm.Model() as model:
    m = pm.Normal('mu', mu=0, sigma=2)
    s = pm.Exponential('s', 1)
 
    pm.Normal("t", mu=m, sigma=s, observed=df['std_num'])

    idata = pm.sample()

_ = az.plot_posterior(idata)


