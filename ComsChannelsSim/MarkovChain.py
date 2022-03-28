"""
Author: Pablo Rivero Lazaro
NIA: 100429366
Date started: 1-12-2021
File version: 1.0
Version date: 7-12-2021

Description:
  This file contains the markov chain class, capable of performing different types of estimations and simulations
  about its own performance and can also simulate itself.
"""

import numpy as np
import random
import ComsChannelsSim.utils as utils
import ComsChannelsSim.ErrorSimulations as errorSim
import math

class markovChain:
  def __init__(self, M, T = None, Π = None, U = None, SNR_average = None, Pe = None, F = None, P = None, averagePe = None):
    """
    Parameters: (Only enter parameters if they are full)
    -M: El número de estados de la cadena de markov a simular
    -T: The probabilities of transition, either from one state to another or to the same state. (Matrix form) [[t00, t10, ..., tX0], [t01, t11, ..., tX1], ..., [t0Y, t1Y, ..., tXY]]
    -U: Umbrals vector (The first and last umbrals not included (0, ..., Inf))
    -SNR_average: In W
    -Π: The probabilities of being on a specific state.
    -Pe: The probabilities of error for each specific state
    - In Gilbert models the state 0 is the good, and the state 1 is the bad
    """
    self.M = M
    if T != None:
      self.T = T
    else:
      self.T = np.zeros((M, M))

    if Π != None:
      self.Π = Π
    else:
      if M == 2 and T != None: # Markov auto calculations
        self.Π = []
        self.Π.append(self.T[0][1]/(self.T[1][0]+self.T[0][1]))
        self.Π.append(self.T[1][0]/(self.T[1][0]+self.T[0][1]))
        self.Π = np.array(self.Π)
      else:
        self.Π = np.zeros(M)

    if U != None:
      self.U = U
      self.U.insert(0, 0)
      self.U.insert(len(self.U), np.Inf)

    else:
      self.U = np.zeros(M+1)

    self.p = SNR_average

    if Pe != None:
      self.Pe = Pe
    else:
      self.Pe = np.zeros(M)

    if F == None:
      if M == 2 and Pe != None: # Markov auto calculations
        self.F = [] # F[bit][row][col]
        self.F.append([[1-self.Pe[0], 0], [0, 1-self.Pe[1]]])
        self.F.append([[self.Pe[0], 0], [0, self.Pe[1]]])
        self.F = np.array(self.F)
    else:
      self.F = np.zeros((2, M, M))

    if P == None: # Markov auto calculations
      if M == 2 and self.F.any() and T != None:
        self.P = [] #P[bit][row][col]
        self.P.append(np.matmul(self.F[0], self.T))
        self.P.append(np.matmul(self.F[1], self.T))
        self.P = np.array(self.P)
    else:
      self.P = np.zeros((2, M, M))

    if averagePe != None:
      self.averagePe = averagePe
    elif Pe != None and self.Π.any():
      self.averagePe = 0
      for ind in range(self.M):
        self.averagePe += self.Π[ind]*self.Pe[ind]
    else:
      self.averagePe = None

  def getT(self, init, end):
    """
    Init is the initial state, which is represented as the row number.
    End is the end state, which is represented as the column number.
    """
    return self.T[end][init]

  def getΠ(self, state):
    return self.Π[state]

  def getΠAll(self):
    return self.Π
  
  def getM(self):
    return self.M

  def getP(self, X):
    return self.P[X]
  
  def setErrorProbabilities(self, Pe):
    self.Pe = Pe
  
  def calculateStateProbabilities(self):
    """
    self.Π * (1*) = 1
    self.Π * self.T = self.Π * I
    """

    a = np.array([], [])
    b = np.array([1, self.Π*np.identity(self.M)])

  def calculateStateProbabilitiesFromUmbrals(self):

    for ind in range(self.M):
      self.Π[ind] = math.exp(-self.U[ind]/self.p)-math.exp(-(self.U[ind+1])/self.p)

  def calculateErrorProbabilitiesFromStateProbabilities(self):

    def calculateGamma(index):
      g = math.exp(-self.U[index]/self.p)*(1-utils.F(math.sqrt(2*self.U[index])))+math.sqrt(self.p/(self.p+1))*utils.F(math.sqrt((2*self.U[index]*(self.p+1))/self.p))
      return g

    for ind in range(self.M):
      self.Pe[ind] = (calculateGamma(ind)-calculateGamma(ind+1))/self.Π[ind]

  def calculateTransitionMatrixFromStateProbabilities(self):
    # Considering "slow fading"
    """a_arr = []
    for ind in range(self.M):

    a = np.array([[], []])
    b = np.array([])

    transitions = np.linalg.solve(a, b)

    for ind in range(self.M):
      self.T[ind] = np"""
    pass
  
  def calculateErrorPattern(self, bitVector):
    """
    The bit vector is defined as a set of zeros and ones that we want to
    calculate how much can appear.
    """

    F0 = np.eye(M)
    F0[0][0] = 1-self.Pe[0]
    F0[1][1] = 1-self.Pe[1]

    F1 = np.eye(M)
    F1[0][0] = self.Pe[0]
    F1[1][1] = self.Pe[1]

    P0 = F0 * self.T
    P1 = F1 * self.T

    for i in bitVector:
      if i == 0:
        P = P * P0
      elif i == 1:
        P = P * P1

    return self.Π * P * np.ones(M, 1)
  
  def calculateErrorNumber(self, totalBits, errorBits):
    """
    totalBits = Number of bits that we have to search
    errorBits = Number of error bits that we want to calculate the probability
    over
    """
    allErrorPatterns = utils.obtainBitCombinations(totalBits, errorBits)

    for errorPattern in allErrorPatterns:
      utils.calculateErrorPattern(errorPattern)
  
  def estimateParametersGilbert(self, errorSequence):
    """
    This function obtains the minimun parameters from a error sequence obtained
    by using the model.
    We can obtain: t01, t10, Pe0
    And we later calculate the rest from these
    """

    # Only for Gilbert model cases
    if self.M == 2:

      # Calculating a, b and c to estimate the model parameters
      a_pattern = np.array([1])
      print(errorSim.estimateErrorProbability(a_pattern, errorSequence))
      b_pattern = np.array([1, 1])
      print(errorSim.estimateErrorProbability(b_pattern, errorSequence))
      c_pattern_0 = np.array([1, 1, 1])
      print(errorSim.estimateErrorProbability(c_pattern_0, errorSequence))
      c_pattern_1 = np.array([1, 0, 1])
      print(errorSim.estimateErrorProbability(c_pattern_1, errorSequence))
      try:
        a = errorSim.estimateErrorProbability(a_pattern, errorSequence)
        print("a: {}".format(a))
        b = errorSim.estimateErrorProbability(b_pattern, errorSequence) / errorSim.estimateErrorProbability(a_pattern, errorSequence)
        print("b: {}".format(b))
        c = errorSim.estimateErrorProbability(c_pattern_0, errorSequence) / ((errorSim.estimateErrorProbability(c_pattern_1, errorSequence) + errorSim.estimateErrorProbability(c_pattern_0, errorSequence)))
        print("c: {}".format(c))
      except ZeroDivisionError:
        print("Try making the number of samples introduced larger")
        return
      
      # Calculating p, h and P
      try:
        p = 1-((a*c-(b**2))/(2*a*c-b*(a+c)))
        h = 1-(b/(1-p))
        P = a*p/((1-h)-a)

        print("p: {:.2f}, h: {:.2f}, P: {:.2f}".format(p, h, P))
      except ZeroDivisionError:
        print("The probability of error is too low")
        return

      #Calculating T and Π matrix
      self.T[0][0] = 1-P
      self.T[0][1] = p
      self.T[1][0] = P
      self.T[1][1] = 1-p

      self.Π[0] = p/(P + p)
      self.Π[1] = P/(P + p)

      self.Pe[0] = 0
      self.Pe[1] = 1-h
  
  def simulateModel(self, iterations, initialState):
    """
    Makes use of a Markov model with all the parameter determined to simulate
    n iterations using the model.

    Parameters:
    * initialState in 0 or 1
    """
    state = initialState
    outputErrorTape = np.zeros(iterations)
    for it in range(iterations):

      # Probability of error
      if random.random() < self.Pe[state]:
        outputErrorTape[it] = 1
      
      # Probability of changing state
      if random.random() > self.T[state][state]:
        if state == 1: state = 0
        else: state = 1

    return outputErrorTape
  
  def printReleventData(self):
    """
    Prints on the terminal the relevant data of the model in an organized
    manner.
    """

    # Printing initial data from the markov model
    print("Markov model with {M} states".format(M = self.M), end='\n')
    if self.M == 2: print("So it is considered a Gilbert model and is treated like so\n", end='\n')

    # Printing information about each of the different states
    for ind in range(self.M):
      if self.M == 2: print("State nº{index} (Good state):".format(index = ind) if ind == 0 else "State nº{index} (Bad state):".format(index = ind))
      else: print("State nº{index}:".format(index = ind))
      print("- Probability of being in the state: {ps}".format(ps = self.Π[ind]))
      print("- Probability of error in the state: {ps}".format(ps = self.Pe[ind]))

    # Printing information baout the differnt transitions
    print("\nTransitions between states:", end='\n')
    for init in range(self.M):
      for end in range(self.M):
        print("- Transition from {init} to {end} with a percentage of {txx}".format(init = init, end = end, txx = self.T[end][init]))

    print("\nAverage probability of error: {:.2f}".format(self.averagePe))

    # Printing information baout the differnt transitions
    if self.M == 2:
      print("\nF matrices:")
      print("F[0]: ")
      for row in self.F[0]:
        for val in row:
            print('{:.2f}'.format(val), end = ', ')
        print()

      print("\nF[1]: ")
      for row in self.F[1]:
        for val in row:
            print('{:.2f}'.format(val), end = ', ')
        print()

      print("\nError probability matrices:")
      print("P[0]: ")
      for row in self.P[0]:
        for val in row:
            print('{:.2f}'.format(val), end = ', ')
        print()

      print("\nP[1]: ")
      for row in self.P[1]:
        for val in row:
            print('{:.2f}'.format(val), end = ', ')
        print()
    
    return None