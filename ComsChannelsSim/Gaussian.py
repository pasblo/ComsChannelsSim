"""
Author: Pablo Rivero Lazaro (Pasblo)
Contact: pasblo39@gmail.com
Version: 1.0
Description:
  This file contains the gaussian class, it allows to interface with the gaussian distribution, being
  able to get probabilities from it, and plotting results.
"""

import numpy as np
import ComsChannelsSim.utils as utils
import scipy.stats as sps
import matplotlib.pyplot as plt

class Gaussian:
  def __init__(self, mean, variance):
    """
    Parameters:
    * mean -> The mean value of the gaussian/normal distribution
    * variance -> The variance of the gaussian/normal distribution
    """

    self.mean = mean
    self.variance = variance
  
  def probabilityNormalizedRange(self, min = np.inf, max = np.inf):
    """
    Calculates the probability of the gaussian defined being between the values
    provided.

    Parameters:
    * Min -> The left most parameter. np.inf is allowed
    * Max -> The right most parameter. np.inf is allowed
    """

    if min != np.inf and max != np.inf:
      if min <= self.mean: minProb = utils.Q(abs(min-self.mean)/self.variance)
      elif min > self.mean: minProb = 1 - utils.Q(abs(min-self.mean)/self.variance)
      if max <= self.mean: maxProb = utils.Q(abs(max-self.mean)/self.variance)
      elif max > self.mean: maxProb = 1 - utils.Q(abs(max-self.mean)/self.variance)

      return abs(minProb - maxProb)
    
    elif min == np.inf and max == np.inf: return 1
    elif min != np.inf: return utils.Q(abs(min-self.mean)/self.variance)
    elif max != np.inf: return 1 - utils.Q(abs(max-self.mean)/self.variance)
  
  def getMean(self):
    return self.mean
  
  def getVariance(self):
    return self.variance
  
  def getStandardDeviation(self):
    return math.sqrt(self.variance)
  
  def plotGaussian(self, lowerBound = -10, upperBound = 10):

    # Calculating the Z transform
    z1 = (lowerBound - self.mean) / self.variance
    z2 = (upperBound - self.mean) / self.variance

    # Calculating the probability
    x = np.arange(z1, z2, 0.001) # range of x in spec
    x_all = np.arange(-10, 10, 0.001) # entire range of x, both in and out of spec
    # mean = 0, stddev = 1, since Z-transform was calculated
    y = sps.norm.pdf(x,0,1)
    y2 = sps.norm.pdf(x_all,0,1)

    # build the plot
    fig, ax = plt.subplots(figsize=(9,6))
    plt.style.use('fivethirtyeight')
    ax.plot(x_all,y2)

    ax.fill_between(x,y,0, alpha=0.3, color='b')
    ax.fill_between(x_all,y2,0, alpha=0.1)
    ax.set_xlim([-4,4])
    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    ax.set_yticklabels([])
    ax.set_title('Normal Gaussian Curve')