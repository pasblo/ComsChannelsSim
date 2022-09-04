"""
Author: Pablo Rivero Lazaro (Pasblo)
Contact: pasblo39@gmail.com
Version: 1.0
Description:
  This file contains an assortment of functions used by other parts of the library, ranging from bit sequence manipulation
  statistical functions, unit conversions and plotting shortcuts.
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import scipy as sp
import math

k = 1.3803e-23 # Boltzman constant

def generateSequenceBits(probabilityOnes, samples):
  """
  Generates a random sequenece of n samples with a probability of generating
  a 1 provided.
  """

  arr = []

  for i in range(samples):
    if random.random() < probabilityOnes:
      arr.append(1)
    else:
      arr.append(0)
  
  return np.array(arr)

def changeZerosByNegatives(sequence):
  newSequence = np.zeros(sequence.size)
  for i in range(sequence.size):
    if sequence[i] == 0:
      newSequence[i] = -1
    else:
      newSequence[i] = 1
  return newSequence

def obtainBitCombinations(total, ones):
  allCombinations = list(itertools.product([0, 1], repeat=total))
  onesCombinations = []
  ind = 0
  for combination in allCombinations:
    if combination.count(1) == ones:
      onesCombinations.append(combination)
      ind += 1
  
  return np.array(onesCombinations)

def Q(input):
  return 0.5 - 0.5*sp.special.erf(input/np.sqrt(2))

def F(input):
  return 1-Q(input)

def NaturalToLogarithmic(natural):
  return 10 * math.log(natural, 10)

def LogarithmicToNatural(logarithmic):
  return math.pow(10, logarithmic/10.0)

def FrequencyToWavelength(frequency, speed = 299792458):
  return speed / frequency

def WavelengthToFrequency(wavelength, speed = 299792458):
  return speed / wavelength

def dB_to_dBm(dB):
  return dB + 30

def dBm_to_dB(dBm):
  return dBm - 30

def plotAxis(ax):
  ax.set_aspect('equal')
  ax.grid(True, which='both')

  # set the x-spine (see below for more info on `set_position`)
  ax.spines['left'].set_position('zero')

  # turn off the right spine/ticks
  ax.spines['right'].set_color('none')
  ax.yaxis.tick_left()

  # set the y-spine
  ax.spines['bottom'].set_position('zero')

  # turn off the top spine/ticks
  ax.spines['top'].set_color('none')
  ax.xaxis.tick_bottom()

def gray_code(bits):
  """
  Generates the gray code for the number of bits indicated
  """
  n = int(bits)
  gray_seq = []
  it = 0
  for i in range(0, 1<<n):
    gray = i^(i>>1)
    gray_seq.append([int(x) for x in bin(gray)[2:]])
    length = len(gray_seq[it])
    for it2 in range(bits-length):
      gray_seq[it].insert(0, 0)
    it += 1
  
  return gray_seq

def calculateSensitivity(**kwargs):
  """
  """
  SNR = kwargs.get("SNR", None)
  SNR_dB = kwargs.get("SNR_dB", None)
  if SNR == None and SNR_dB != None: SNR = LogarithmicToNatural(SNR_dB)
  elif SNR == None and SNR_dB == None: raise Exception("SNR parameter is missing")

  return SNR * claculateNoisePower(**kwargs)

def claculateNoisePower(**kwargs):
  """
  """

  equivalentTemperature = kwargs.get("equivalentTemperature", None)
  if equivalentTemperature == None: raise Exception("Equivalent temperature parameter is missing")

  bandwith = kwargs.get("bandwith", None)
  if bandwith == None: raise Exception("Bandwith parameter is missing")

  return k * equivalentTemperature * bandwith

def arrayToString(npArray):
  string = ""
  for num in npArray:
    string += str(num)

  return string

def stringToArray(string):
  arr = []
  for char in string:
    arr.append(int(char))
  return np.array(arr)

def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
    """Calculate the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    """
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ''.join(input_padded_array)[len_input:]

def crc_check(input_bitstring, polynomial_bitstring, check_value):
    """Calculate the CRC check of a string of bits using a chosen polynomial."""
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ('1' not in ''.join(input_padded_array)[len_input:])

def generatePacket(size):
  return generateSequenceBits(0.5, size)

def calculateCRC(bitTape, BCH_code):
  data_binstr = arrayToString(bitTape)
  BCH_code_binstr = "{0:b}".format(BCH_code)
  return crc_remainder(data_binstr, BCH_code_binstr, '0')

def addCRC(bitTape, BCH_code):
  CRC_extra = calculateCRC(bitTape, BCH_code)
  CRC_extra_arr = stringToArray(CRC_extra)
  return np.concatenate((bitTape, CRC_extra_arr))

def checkCRC(bitTape, BCH_code, k):
  data_binstr = arrayToString(bitTape)
  BCH_code_binstr = "{0:b}".format(BCH_code)
  extracted_data = data_binstr[:k]
  extracted_CRC = data_binstr[-(len(data_binstr)-k):]
  return crc_check(extracted_data, BCH_code_binstr, extracted_CRC)

def binAdd(a, b, carry = False):
  sol = []
  for ind in range(len(a)):
    if a[ind] and b[ind]: sol.append(0)
    elif not a[ind] and not b[ind]: sol.append(0)
    else: sol.append(1)

  return np.array(sol)

def probErrorInBurst(errors, burst, P0, P1):

  if errors == burst: return np.power(P1, burst)
  elif errors == 0: return np.power(P0, burst)
  else: return P0*probErrorInBurst(errors, burst-1, P0, P1)+P1*probErrorInBurst(errors-1, burst-1, P0, P1)