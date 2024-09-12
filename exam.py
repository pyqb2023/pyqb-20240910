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

pass

# ### Exercise 2 (max 5 points)
#
# Consider the **set** of the letters appearing in the genome string. Compute all the triplets that *can* be composed by using these letters (for example: `'AAC'`), by considering each and its reverse only once: for example, only one between `'AAC'` and `'CAA'` should appear in the result. Name the result `potential_triplets`.

pass

# ### Exercise 3 (max 7 points)
#
# Define a function which takes a string of arbitrary length ($\ge 3$) and a triplet, and returns the number of occurrences of the triplet or its reverse in the string. For example the triplet `'AAT'` occurs three times (twice as `'AAT'` and once as `'TAA'`) in `'CAATAATCC'` and the triplet `'AAA'` occurs five times in `'AAAAAAA'`.
#
# To get the full marks, you should declare correctly the type hints (the signature of the function) and add a doctest string.

pass

# import doctest
# doctest.testmod()


# ### Exercise 4 (max 5 points)
#
# Define a pandas DataFrame indexed by all the potential triplets identified in Exercise 2, with a column reporting the occurrences of each triplet in the genome under analysis. For example, the triplet `'AGG'` should have 356 occurrences. Add a column `even`, with a value of `True` if the number of occurrences is even and `False` otherwise.

pass

# ### Exercise 5 (max 2 points)
#
# Add a column with the "standardized number of occurrences" `std_num` of each triplet. The *standardized number of occurrences* is defined as the difference between a value and the mean over all the values, divided by the standard deviation over all the values. 

pass

# ### Exercise 6 (max 3 points)
#
# Plot a histogram of the values `std_num` using a list `[-3, -2.5, -2, ..., 2, 2.5, 3]` to define 12 bins. Add to the figure also a red dashed vertical line marking the mean.
#

pass

# ### Exercise 7 (max 5 points)
#
#
# Plot two histograms (two different plots on one horizontal row, add also a legend to the figure), one for the triplets occuring an even number of times, one for the others. The two histograms should depict the values in increasing order.

pass

# ### Exercise 8 (max 4 points)
#
# Consider this statistical model: the *standardized number of occurrences* of even and not even triplets is normally distributed, with an unknown mean, and an unknown standard deviation. Your *a priori* estimation of the mean is given by a normal distribution with mean 0 and standard deviation 2; your prior estimation for the standard deviation is an exponential distribution with $\lambda = 1$. Use PyMC to sample the posterior distributions after having seen the actual values for even and not even triplets.  Plot the posterior distributions with `az.plot_posterior`.

pass
