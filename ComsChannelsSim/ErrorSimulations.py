"""
Description:
  This file contains an assortment of functions used to simulate different probabilities in error sequences.
"""

import numpy as np
import ComsChannelsSim.utils as utils

def simulateErrorPatternProbability(errorProbability, samples, errorPattern):
  """
  """

  # Generating the array of bits with the error probability
  errors = utils.generateSequenceBits(errorProbability, samples)
  
  # Making the convolution between the array of bits and the pattern
  newZeros = utils.changeZerosByNegatives(errors)
  newPattern = utils.changeZerosByNegatives(errorPattern)
  
  conv = np.convolve(newZeros, newPattern)

  # Searching for coincidences in the error pattern
  errorPatternCoincidences = 0
  for i in range(conv.size):
    if conv[i] == errorPattern.size:
      errorPatternCoincidences += 1
  
  return errorPatternCoincidences/samples

def simulateErrorNumberProbability(errorProbability, samples, errorBits):
  """
  Simulates the probability of obtaining the exact number of error bits
  """

  allErrorPatterns = utils.obtainBitCombinations(errorBits, errorBits)
  totalProbability = 0

  for errorPattern in allErrorPatterns:
    totalProbability += utils.simulateErrorPatternProbability(errorProbability, samples, errorPattern)
  
  return totalProbability

def estimateErrorProbability(errorPattern, errorSequence):
  """
  Counting the number of times the error pattern occurs and then dividing it by
  the total number of elements on the sequence.
  """

  N = len(errorPattern)
  possibles = np.where(errorSequence == errorPattern[0])[0]

  findings = []
  for p in possibles:
      check = errorSequence[p:p+N]
      if np.all(check == errorPattern):
          findings.append(p)
  
  return len(findings)/len(errorSequence)