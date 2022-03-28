"""
Author: Pablo Rivero Lazaro
NIA: 100429366
Date started: 1-12-2021
File version: 1.0
Version date: 7-12-2021

Description:
  This file contains a class for simulating the channel element in a comunication system, it can simulate
  how different attenuations affect the power, probabilities of error, and simulate bit by bit error.
"""

import numpy as np
import komm
import math
import matplotlib.pyplot as plt
import cmath
import ComsChannelsSim.utils as utils
import ComsChannelsSim.Gaussian as Gaussian

class channelElement:
  def __init__(self, type, **kwargs):
    """
    Parameters:
    * type -> The type of channel used {AWGN, DMC, BSC, BEC}
    * snr -> The signal to noise ratio (Natural units)
    * signal power -> The transmitted signal power
    * band -> The type of band used by the channel {BB, PB}
    """

    self.type = type
    self.snr = kwargs.get("snr", np.inf)
    self.noisePower = kwargs.get("noisePower", 0.0)
    self.signalPower = kwargs.get("signalPower", 1.0)
    self.band = kwargs.get("band", "BB")
    self.transitionMatrix = kwargs.get("transitionMatrix", None)
    self.crossoverProbability = kwargs.get("crossoverProbability", 0.0)
    self.erasureProbability = kwargs.get("erasureProbability", 0.0)

    # Completing the parameters if possible
    if self.snr != np.inf and self.noisePower != 0.0:
      self.signalPower = self.snr * self.noisePower
    
    elif self.snr != np.inf and self.signalPower != 1.0:
      self.noisePower = self.signalPower / self.snr
    
    elif self.signalPower != 1.0 and self.noisePower != 0.0:
      self.snr = self.signalPower / self.noisePower

    # Violations
    if self.type == "DMC" and self.transitionMatrix == None: raise Exception("Transition matrix parameter is missing")

    if self.type == "AWGN": self.model = komm.AWGNChannel(self.snr, self.signalPower)
    elif self.type == "DMC": self.model = komm.DiscreteMemorylessChannel(self.transitionMatrix)
    elif self.type == "BSC": self.model = komm.BinarySymmetricChannel(self.crossoverProbability)
    elif self.type == "BEC": self.model = komm.BinaryErasureChannel(self.erasureProbability)
    else: self.model = None

    # Declaring the attenuation arrays
    self.totalAttenuation_dB = 0
    self.attenuationErrorModel = 0
    self.totalGain_dB = 0
  
  def getCapacity(self):
    return self.model.capacity()
  
  def generateNoise(self, N):
    if self.type == "AWGN":
      if self.band == "BB":
        noise = [math.sqrt(self.noisePower/2) * random.random() for it in range(N)]
      
      elif self.band == "PB":
        noise_I = [math.sqrt(self.noisePower/2) * random.random() for it in range(N)]
        noise_Q = [math.sqrt(self.noisePower/2) * random.random() for it in range(N)]
        noise = [complex(noise_I[it], noise_Q[it]) for it in range(N)]

    return noise
  
  def friisAttenuation(self, distance, **kwargs):
    """
    Calculates the attenuation to the transmission produced by the propagation of the signal,
    it uses the friis formula to do so.

    Parameters:
    * distance -> The distance between the point of emission and the point to calculate attenuation [m]
    * wavelength -> The wavelength of the signal being transmitted [m]
    * n -> Pathloss exponent [No units]

    Returns:
    * Afriis -> The attenuation losses [dB]
    """
    wavelength = kwargs.get("wavelength", None)
    n = kwargs.get("n", 2)

    if wavelength == None or distance == None: raise Exception("Parameters missing")

    return utils.NaturalToLogarithmic(math.pow((4*math.pi*distance)/(wavelength), n)) # Friis formula to obtain attenuation in dB
  
  def hataUrbanAttenuation(self, distance, **kwargs):
    """
    Calculates the attenuation to the transmission produced by the propagation of the signal in urban areas, 
    it uses the Okumura-Hata model to do so.

    Parameters:
    * distance -> The distance between the point of emission and the point to calculate attenuation [m]
    * baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
    * mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
    * frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    * correctionFactorApplied -> The antenna height correction factor used in the formula, options:
      - "Small-Medium city" -> Optimized for small or medium sized cities
      - "Large city" -> Optimized for large cities
    
    Returns:
    * Ahata -> The attenuation losses [dB]
    # This is dedicated to you my love uint8_t, this was programmed that day 3-12-2021
    """

    baseHeight = kwargs.get("baseHeight", None)
    mobileHeight = kwargs.get("mobileHeight", None)
    frequency = kwargs.get("frequency", None)
    correctionFactorApplied = kwargs.get("correctionFactorApplied", "Small-Medium city")
    if baseHeight == None or mobileHeight == None or frequency == None or distance == None: raise Exception("Parameters missing")

    if correctionFactorApplied == "Small-Medium city": correctionFactor = 0.8 + (1.1*math.log(frequency, 10)-0.7)*mobileHeight-1.56*math.log(frequency, 10)
    elif correctionFactorApplied == "Large city":
      if frequency <= 200: correctionFactor = 8.29*math.pow(math.log(1.54*mobileHeight, 10), 2)-1.1
      elif frequency > 200: correctionFactor = 3.2*math.pow(math.log(11.75*mobileHeight, 10), 2)-4.97
      else: raise Exception("Unexpected exception, too bad")

    return 69.55+26.16*math.log(frequency, 10)-13.82*math.log(baseHeight, 10)-correctionFactor+(44.9-6.55*math.log(baseHeight, 10))*math.log(distance/1000.0, 10)
  
  def hataSuburbanAttenuation(self, distance, **kwargs):
    """
    Calculates the attenuation to the transmission produced by the propagation of the signal in suburban areas, 
    it uses the Okumura-Hata model to do so.

    Parameters:
    * distance -> The distance between the point of emission and the point to calculate attenuation [m]
    * baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
    * mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
    * frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    
    Returns:
    * Ahata -> The attenuation losses [dB]
    """

    baseHeight = kwargs.get("baseHeight", None)
    mobileHeight = kwargs.get("mobileHeight", None)
    frequency = kwargs.get("frequency", None)

    if baseHeight == None or mobileHeight == None or frequency == None or distance == None: raise Exception("Parameters missing")

    return self.hataUrbanAttenuation(distance, baseHeight, mobileHeight, frequency) - 2*math.pow(math.log(frequency/28, 10), 2) - 5.4
  
  def hataOpenAttenuation(self, distance, **kwargs):
    """
    Calculates the attenuation to the transmission produced by the propagation of the signal in opem areas, 
    it uses the Okumura-Hata model to do so.

    Parameters:
    * distance -> The distance between the point of emission and the point to calculate attenuation [m]
    * baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
    * mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
    * frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    
    Returns:
    * Ahata -> The attenuation losses by path-lass [dB]
    """

    baseHeight = kwargs.get("baseHeight", None)
    mobileHeight = kwargs.get("mobileHeight", None)
    frequency = kwargs.get("frequency", None)

    if baseHeight == None or mobileHeight == None or frequency == None or distance == None: raise Exception("Parameters missing")

    return self.hataUrbanAttenuation(distance, baseHeight, mobileHeight, frequency) - 4.78*math.pow(math.log(frequency, 10), 2) + 18.33*math.log(frequency, 10) - 40.94

  def acusticAttenuation(self, distance, **kwargs): # NOT WORKING
    """
    Calculates the attenuation to the transmission produced by an acustic channel.

    Parameters:
    * 
    
    Returns:
    * Aacustic -> The attenuation losses by path-lass [dB]
    """

    frequency = kwargs.get("frequency", None)
    if frequency == None: raise Exception("Frequency parameter is missing")

    a = 0.11*(frequency**2)/(1+frequency**2)+44*(frequency**2)/(4100+frequency**2)+2.75e-4*frequency**2
    return -20*math.log(distance, 10) - a*distance

  def fresnelToAttenuation(self, v, Fbase = None):
    """
    Returns the attenuation that is related to the fresnel diffraction parameter.

    Parameters:
    * v -> Fresnel difraction parameter

    Returns:
    * Adiff -> The attenuation by diffraction [dB]
    """
    F = 0
    if Fbase != None:
      v_vector = np.arange(-5, 95, 0.01)
      new_v_vector = []
      for nv in range(v_vector.size):
        new_v_vector.append(cmath.exp(complex(0, -1)*math.pi*(v_vector[nv]**2)/2))

      F0 = (complex(1, 1)/2)*np.sum(new_v_vector)

    else:
      F0 = Fbase

    v_vector = np.arange(v, v+100, 0.01)
    new_v_vector = []
    for nv in range(v_vector.size):
      new_v_vector.append(cmath.exp(complex(0, -1)*math.pi*(v_vector[nv]**2)/2))

    F = (complex(1, 1)/2)*np.sum(new_v_vector)
    F = 2*utils.NaturalToLogarithmic(abs(F)/abs(F0))

    return F*-1 # To convert it to attenuation

  def diffractionAttenuation(self, txDistanceObject, rxDistanceObject, relativeHeight, wavelength):
    """
    Calculates the attenuation to the transmission produced by diffraction by an object, that is
    in the path of the comunication.

    Parameters:
    * txDistanceObject -> The distance between the transmissor and the object in the path of the transmission. [m]
    * rxDistanceObject -> The distance between the receiver and the object in the path of the transmission. [m]
    * relativeHeight -> The relative height between the antennas and the highest part of the object (Negative if above the object) [m]
    * wavelength -> The wavelength of the signal being transmitted [m]

    Returns:
    * Adiff -> The attenuation losses by diffraction [dB]
    """

    fresnelParameter = relativeHeight*math.sqrt((2*(txDistanceObject+rxDistanceObject))/(wavelength*txDistanceObject*rxDistanceObject))
    return self.fresnelToAttenuation(fresnelParameter)
  
  def lossAttenuation(self, distance, **kwargs):
    """
    Calculates the loss attenuation at a given distance using a specific model

    Parameters:
    * distance -> The distance of the receiver from the transmitter [m]
    * lossModel -> The model we want to use to calculate path loss attenuation {"friis", "hataUrban", "hataSuburban", "hataOpen"}
    * If friis:
      - wavelength -> The wavelength of the signal being transmitted [m]
      - n(?) -> Pathloss exponent [No units]
    
    * If hataUrban:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
      - correctionFactorApplied -> The antenna height correction factor used in the formula, options:
        - "Small-Medium city" -> Optimized for small or medium sized cities
        - "Large city" -> Optimized for large cities
    
    * If hataSuburban / hataOpen:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]

    * If acusticChannel
      - 
    """
    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    lossAttenuation = 0

    if lossModel == "friis": lossAttenuation = self.friisAttenuation(distance, **kwargs)
    elif lossModel == "hataUrban": lossAttenuation = self.hataUrbanAttenuation(distance, **kwargs)
    elif lossModel == "hataSuburban": lossAttenuation = self.hataSuburbanAttenuation(distance, **kwargs)
    elif lossModel == "hataOpen": lossAttenuation = self.hataOpenAttenuation(distance, **kwargs)
    elif lossModel == "acusticChannel": raise Exception("Model is not working")# lossAttenuation = self.acusticAttenuation(distance, **kwargs)
    else: raise Exception("Loss model not supported")

    return lossAttenuation

  def calculateDifractionAttenuationFresnel(self, fresnelParameter):

    v_vector = np.arange(-4, -4+100, 0.01)
    new_v_vector = []
    for nv in range(v_vector.size):
      new_v_vector.append(cmath.exp(complex(0, -1)*math.pi*(v_vector[nv]**2)/2))
    difractionAttenuationBase = (complex(1, 1)/2)*np.sum(new_v_vector)
        
    v_vector = np.arange(fresnelParameter, fresnelParameter+100, 0.01)
    new_v_vector = []
    for nv in range(v_vector.size):
      new_v_vector.append(cmath.exp(complex(0, -1)*math.pi*(v_vector[nv]**2)/2))

    difractionAttenuation = (complex(1, 1)/2)*np.sum(new_v_vector)
    if fresnelParameter != -4: difractionAttenuation = -2*utils.NaturalToLogarithmic(abs(difractionAttenuation)/abs(difractionAttenuationBase))
    else: difractionAttenuation = 2*utils.NaturalToLogarithmic(1)

    return difractionAttenuation

  def diffractionAttenuation(self, **kwargs):

    rx_distance = kwargs.get("rx_distance", None)
    if rx_distance == None: raise Exception("Rx distance parameter is missing")

    tx_distance = kwargs.get("tx_distance", None)
    if tx_distance == None: raise Exception("Tx distance parameter is missing")

    distance_to_peak = kwargs.get("distance_to_peak", None) # Below the peak is greater than 0, above the peak is smaller than 0
    if distance_to_peak == None: raise Exception("Distance to peak parameter is missing")

    wavelength = kwargs.get("wavelength", None)
    if wavelength == None: raise Exception("Wavelength parameter is missing")

    fresnelParameter = distance_to_peak*math.sqrt((2*(tx_distance+rx_distance))/(wavelength*tx_distance*rx_distance))
    return self.calculateDifractionAttenuationFresnel(fresnelParameter)

  def calculateDistance_attenuation(self, **kwargs):

    attenuation_objetive = kwargs.get("attenuation_objetive", None)
    if attenuation_objetive == None: raise Exception("Loss model parameter is missing")

    ndigits = kwargs.get("ndigits", 9)

    attenuation = -1
    distance_testing = 1
    factor = 100.0
    prev_action = 0 # 0 stands for distance inc, 1 stands for distance dec
    action = 0
    while round(attenuation_objetive, ndigits) != round(attenuation, ndigits):
      # Calculating the new loss attenuation
      attenuation = self.lossAttenuation(distance = distance_testing, **kwargs)
      #print("For length {}, we have attenuation {}, with received power {}".format(distance_testing, self.totalAttenuation, receivedPower))

      # Calculating the new distance
      if attenuation_objetive > attenuation:
        action = 0
        distance_testing += factor

      else:
        action = 1
        distance_testing -= factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action

    return distance_testing
  
  def addAttenuation(self, **kwargs):
    """
    Adds an attenuation to the channel

    Parameters:
    * attenuation -> The attenuation to be added to the total attenuation (positive) [W] or [dB]
    """
    attenuation = kwargs.get("attenuation", None)
    attenuation_dB = kwargs.get("attenuation_dB", None)
    if attenuation_dB == None and attenuation != None: attenuation_dB = utils.NaturalToLogarithmic(attenuation)
    elif attenuation_dB == None and attenuation == None: raise Exception("Attenuation parameter is missing")

    self.totalAttenuation_dB += attenuation_dB
  
  def setAttenuations(self, **kwargs):
    """
    Set the attenuation of the total channel to the sepecified parameter, if nothing is passed as argument the total attenuation is set to 0

    Parameters:
    * attenuation -> The attenuation to set the total attenuation (positive) [W] or [dB]
    """
    attenuation = kwargs.get("attenuation", None)
    attenuation_dB = kwargs.get("attenuation_dB", 0)
    if attenuation_dB == None and attenuation != None: attenuation_dB = utils.NaturalToLogarithmic(attenuation)
    elif attenuation_dB == None and attenuation == None: raise Exception("Attenuation parameter is missing")

    self.totalAttenuation_dB = attenuation_dB
  
  def addGain(self, **kwargs):
    """
    Adds a gain to the channel

    Parameters:
    * gain -> The gain to to be added to the total gain (positive) [W] or [dB]
    """
    gain = kwargs.get("gain", None)
    gain_dB = kwargs.get("gain_dB", None)
    if gain_dB == None and gain != None: gain_dB = utils.NaturalToLogarithmic(gain)
    elif gain_dB == None and gain == None: raise Exception("Gain parameter is missing")

    self.totalGain_dB += gain_dB
  
  def setGains(self, **kwargs):
    """
    Set the gain of the total channel to the sepecified parameter, if nothing is passed as argument the total gain is set to 0
    
    Parameters:
    * gain -> The gain to set the total gain (positive) [W] or [dB]
    """
    gain = kwargs.get("gain", None)
    gain_dB = kwargs.get("gain_dB", 0)
    if gain_dB == None and gain != None: gain_dB = utils.NaturalToLogarithmic(gain)
    elif gain_dB == None and gain == None: raise Exception("Gain parameter is missing")

    self.totalGain_dB = gain_dB
  
  def calculateRecivedPower(self, **kwargs):
    """
    Calculates the received power with a given transmitted power, all attenuations and gains must have been added previously
    
    Parameters:
    * transmittedPower -> The transmitted power by the transmitting station [W] or [dB]

    Returns:
    * receivedPower -> The recived power at a distance from the transmitter [dB]
    """
    transmittedPower = kwargs.get("transmittedPower", None)
    transmittedPower_dB = kwargs.get("transmittedPower_dB", None)
    if transmittedPower_dB == None and transmittedPower != None: transmittedPower_dB = utils.NaturalToLogarithmic(transmittedPower)
    elif transmittedPower_dB == None and transmittedPower == None: raise Exception("Transmitted power parameter is missing")

    return transmittedPower_dB + self.totalGain_dB - self.totalAttenuation_dB

  def calculateTransmittedPower(self, **kwargs):
    """
    Calculates the transmitted power with a given received power, all attenuations and gains must have been added previously
    
    Parameters:
    * receivedPower -> The recived power at a distance from the transmitter [W] or [dB]

    Returns:
    * transmittedPower -> The transmitted power by the transmitting station [dB]
    """
    receivedPower = kwargs.get("receivedPower", None)
    receivedPower_dB = kwargs.get("receivedPower_dB", None)
    if receivedPower_dB == None and receivedPower != None: receivedPower_dB = utils.NaturalToLogarithmic(receivedPower)
    elif receivedPower_dB == None and receivedPower == None: raise Exception("Received power parameter is missing")

    return receivedPower_dB - self.totalGain_dB + self.totalAttenuation_dB
  
  def calculateDisponibility(self, **kwargs):
    """
    Calculating the disponibility of the channel. The probability that it works

    Parameters:
    * receivedPower -> The recived power at a distance from the transmitter [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * standardDeviation -> The standard deviation of the gaussian error that is in the attenuation of the channel [dB]

    Returns:
    * disponibility -> The disponibility of the comunication taking into account the attenuation error model
    """
    receivedPower = kwargs.get("receivedPower", None)
    receivedPower_dB = kwargs.get("receivedPower_dB", None)
    if receivedPower_dB == None and receivedPower != None: receivedPower_dB = utils.NaturalToLogarithmic(receivedPower)
    elif receivedPower_dB == None and receivedPower == None: raise Exception("Received power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    standardDeviation = kwargs.get("standardDeviation", None)
    if standardDeviation == None: raise Exception("Standard deviation parameter is missing")

    errorModel = Gaussian.Gaussian(receivedPower_dB, math.pow(standardDeviation, 2))
    return errorModel.probabilityNormalizedRange(max = sensitivity_dB)

  def calculateReceivedPower_disponibility(self, **kwargs):

    disponibility_objetive = kwargs.get("disponibility_objetive", None)
    if disponibility_objetive == None: raise Exception("Disponibility parameter is missing")

    ndigits = kwargs.get("ndigits", 9)

    disponibility = -1
    receivedPower_testing = 1
    factor = 1.0
    prev_action = 0 # 0 stands for distance inc, 1 stands for distance dec
    action = 0
    while round(disponibility_objetive, ndigits) != round(disponibility, ndigits):
      # Calculating the new loss attenuation
      disponibility = self.calculateDisponibility(receivedPower_dB = receivedPower_testing, **kwargs)
      #print("For length {}, we have attenuation {}, with received power {}".format(distance_testing, self.totalAttenuation, receivedPower))

      # Calculating the new distance
      if disponibility_objetive > disponibility:
        action = 0
        receivedPower_testing += factor

      else:
        action = 1
        receivedPower_testing -= factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action

    return receivedPower_testing
  
  def calculateIndisponibility(self, **kwargs):
    """
    Calculating the indisponibility of the channel. The probability it does not work

    Parameters:
    * receivedPower -> The recived power at a distance from the transmitter [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * standardDeviation -> The standard deviation of the gaussian error that is in the attenuation of the channel [dB]

    Returns:
    * disponibility -> The disponibility of the comunication taking into account the attenuation error model
    """
    receivedPower = kwargs.get("receivedPower", None)
    receivedPower_dB = kwargs.get("receivedPower_dB", None)
    if receivedPower_dB == None and receivedPower != None: receivedPower_dB = utils.NaturalToLogarithmic(receivedPower)
    elif receivedPower_dB == None and receivedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    standardDeviation = kwargs.get("standardDeviation", None)
    if standardDeviation == None: raise Exception("Standard deviation parameter is missing")

    errorModel = Gaussian.Gaussian(receivedPower_dB, math.pow(standardDeviation, 2))
    return errorModel.probabilityNormalizedRange(min = sensitivity_dB)
  
  def calculateLinkMargin(self, **kwargs):
    """
    Calculates the link margin of a comunicacion knowing the received power and the sensitivity.

    Parameters:
    * receivedPower -> The recived power at a distance from the transmitter [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]

    Returns:
    * linkMargin -> The difference between the minimum expected power received at the receiver's end, and the receiver's sensitivity [dB]
    """
    receivedPower = kwargs.get("receivedPower", None)
    receivedPower_dB = kwargs.get("receivedPower_dB", None)
    if receivedPower_dB == None and receivedPower != None: receivedPower_dB = utils.NaturalToLogarithmic(receivedPower)
    elif receivedPower_dB == None and receivedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    return abs(receivedPower_dB - sensitivity_dB)
  
  def calculateReachProbability(self, **kwargs):
    """
    Calculates the probability of error for the transmission at a given distance.

    Parameters:
    * transmittedPower -> The transmitted power by the transmitting station [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * standardDeviation_dB -> The standard deviation of the gaussian error that is in the attenuation of the channel [dB]

    Returns:
    * reachProbability -> The probability that can be achieved [%]
    """
    transmittedPower = kwargs.get("transmittedPower", None)
    transmittedPower_dB = kwargs.get("transmittedPower_dB", None)
    if transmittedPower_dB == None and transmittedPower != None: transmittedPower_dB = utils.NaturalToLogarithmic(transmittedPower)
    elif transmittedPower_dB == None and transmittedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    standardDeviation_dB = kwargs.get("standardDeviation_dB", None)
    if standardDeviation_dB == None: raise Exception("Standard deviation parameter is missing")
    
    # All attenuations of path loss must have been added previous to this
    receivedPower_dB = self.calculateRecivedPower(transmittedPower_dB = transmittedPower_dB)
    errorModel = Gaussian.Gaussian(receivedPower_dB, math.pow(standardDeviation_dB, 2))
    #print("Received power {}, sensitivity {}".format(receivedPower_dB, sensitivity_dB))
    if receivedPower_dB < sensitivity_dB: errorProbability = 0.5
    else: errorProbability = errorModel.probabilityNormalizedRange(min = sensitivity_dB)
    return errorProbability
  
  def calculateDistance_sensitivity(self, **kwargs):
    """
    Distance maximun taking into account only the sensitivity, the power received must be the same as the sensitivity.

    Parameters:
    * transmittedPower -> The transmitted power by the transmitting station [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * lossModel -> The model we want to use to calculate path loss attenuation {"friis", "hataUrban", "hataSuburban", "hataOpen"}
    * If friis:
      - wavelength -> The wavelength of the signal being transmitted [m]
      - n(?) -> Pathloss exponent [No units]
    
    * If hataUrban:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
      - correctionFactorApplied -> The antenna height correction factor used in the formula, options:
        - "Small-Medium city" -> Optimized for small or medium sized cities
        - "Large city" -> Optimized for large cities
    
    * If hataSuburban / hataOpen:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    
    Returns:
    * distance -> The distance obtained [m]
    """
    transmittedPower = kwargs.get("transmittedPower", None)
    transmittedPower_dB = kwargs.get("transmittedPower_dB", None)
    if transmittedPower_dB == None and transmittedPower != None: transmittedPower_dB = utils.NaturalToLogarithmic(transmittedPower)
    elif transmittedPower_dB == None and transmittedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    ndigits = kwargs.get("ndigits", 9)

    standardAttenuation_dB = self.totalAttenuation_dB
    # print("Base attenuation: {:.2f}dB".format(standardAttenuation_dB))

    receivedPower_dB = -1
    distance_testing = 1
    factor = 1000.0
    prev_action = 0 # 0 stands for distance inc, 1 stands for distance dec
    action = 0
    while round(sensitivity_dB, ndigits) != round(receivedPower_dB, ndigits):
      # Calculating the new loss attenuation
      self.setAttenuations(attenuation_dB = standardAttenuation_dB)
      self.addAttenuation(attenuation_dB = self.lossAttenuation(distance = distance_testing, **kwargs))
      receivedPower_dB = self.calculateRecivedPower(transmittedPower_dB = transmittedPower_dB)
      # print("For length {}m, we have attenuation {}dB, with received power {}dB".format(distance_testing, self.totalAttenuation_dB, receivedPower_dB))

      # Calculating the new distance
      if receivedPower_dB > sensitivity_dB:
        action = 0
        distance_testing += factor

      else:
        action = 1
        distance_testing -= factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action
    
    # Resetting the attenuation to the begining
    self.setAttenuations(attenuation_dB = standardAttenuation_dB)

    return distance_testing
  
  def calculateDistance_reachProbability(self, **kwargs):
    """
    All non path loss attenuations and gains must have been added prevous to this method. Calculates the
    maximun distance that can be reached with the probability of error indicated as maximun.

    Parameter:
    * transmittedPower -> The transmitted power by the transmitting station [W] or [dB]
    * reachProbability -> The probability we want to achieve [%]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * standardDeviation_dB -> The standard deviation of the gaussian error that is in the attenuation of the channel [dB]
    * lossModel -> The model we want to use to calculate path loss attenuation {"friis", "hataUrban", "hataSuburban", "hataOpen"}
    * If friis:
      - wavelength -> The wavelength of the signal being transmitted [m]
      - n(?) -> Pathloss exponent [No units]
    
    * If hataUrban:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
      - correctionFactorApplied -> The antenna height correction factor used in the formula, options:
        - "Small-Medium city" -> Optimized for small or medium sized cities
        - "Large city" -> Optimized for large cities
    
    * If hataSuburban / hataOpen:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    
    Returns:
    * distance -> The distance obtained [m]
    """
    transmittedPower = kwargs.get("transmittedPower", None)
    transmittedPower_dB = kwargs.get("transmittedPower_dB", None)
    if transmittedPower_dB == None and transmittedPower != None: transmittedPower_dB = utils.NaturalToLogarithmic(transmittedPower)
    elif transmittedPower_dB == None and transmittedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    reachProbability = kwargs.get("reachProbability", None)
    if reachProbability == None: raise Exception("Reach probability parameter is missing")

    standardDeviation_dB = kwargs.get("standardDeviation_dB", None)
    if standardDeviation_dB == None: raise Exception("Standard deviation parameter is missing")

    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    ndigits = kwargs.get("ndigits", 9)

    standardAttenuation = self.totalAttenuation_dB

    probability_obatained = 0
    distance_testing = 1
    factor = 1000.0
    prev_action = 0 # 0 stands for distance dec, 1 stands for distance inc
    action = 0
    while round(probability_obatained, ndigits) != round(reachProbability, ndigits):
      # Calculating the new attenuation
      self.setAttenuations(attenuation_dB = standardAttenuation)
      self.addAttenuation(attenuation_dB = self.lossAttenuation(distance = distance_testing, **kwargs))
      probability_obatained = self.calculateReachProbability(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, standardDeviation_dB = standardDeviation_dB)
      #print("For length {}, we have attenuation {}, with error probability {}".format(distance_testing, self.totalAttenuation_dB, probability_obatained))
      #time.sleep(0.1)
      # Calculating the new distance
      if probability_obatained > reachProbability:
        action = 0
        distance_testing -= factor
      else:
        action = 1
        distance_testing += factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action
    
    # Resetting the attenuation to the begining
    self.setAttenuations(attenuation_dB = standardAttenuation)

    return distance_testing

  def calculatePower_reachProbability(self, **kwargs):
    """
    All non path loss attenuations and gains must have been added prevous to this method. Calculates the
    maximun distance that can be reached with the probability of error indicated as maximun.

    Parameter:
    * distance -> The distance from transmitter to receiver [m]
    * reachProbability -> The probability we want to achieve [%]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * standardDeviation_dB -> The standard deviation of the gaussian error that is in the attenuation of the channel [dB]
    * lossModel -> The model we want to use to calculate path loss attenuation {"friis", "hataUrban", "hataSuburban", "hataOpen"}
    * If friis:
      - wavelength -> The wavelength of the signal being transmitted [m]
      - n(?) -> Pathloss exponent [No units]
    
    * If hataUrban:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
      - correctionFactorApplied -> The antenna height correction factor used in the formula, options:
        - "Small-Medium city" -> Optimized for small or medium sized cities
        - "Large city" -> Optimized for large cities
    
    * If hataSuburban / hataOpen:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    
    Returns:
    * transmittedPower -> The transmitted power by the transmitting station [dB]
    """

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    distance = kwargs.get("distance", None)
    if distance == None: raise Exception("Distance parameter is missing")

    reachProbability = kwargs.get("reachProbability", None)
    if reachProbability == None: raise Exception("Reach probability parameter is missing")

    standardDeviation_dB = kwargs.get("standardDeviation_dB", None)
    if standardDeviation_dB == None: raise Exception("Standard deviation parameter is missing")

    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    ndigits = kwargs.get("ndigits", 9)

    standardAttenuation = self.totalAttenuation_dB

    probability_obatained = 0
    transmittedPower_testing = 1
    factor = 1.0
    prev_action = 0 # 0 stands for distance dec, 1 stands for distance inc
    action = 0
    while round(probability_obatained, ndigits) != round(reachProbability, ndigits):
      # Calculating the new attenuation
      self.setAttenuations(attenuation_dB = standardAttenuation)
      self.addAttenuation(attenuation_dB = self.lossAttenuation(**kwargs))
      probability_obatained = self.calculateReachProbability(transmittedPower_dB = transmittedPower_testing, sensitivity_dB = sensitivity_dB, standardDeviation_dB = standardDeviation_dB)
      #print("For length {}, we have attenuation {}, with error probability {}".format(transmittedPower_testing, self.totalAttenuation_dB, probability_obatained))
      #time.sleep(0.1)
      # Calculating the new distance
      if probability_obatained < reachProbability:
        action = 0
        transmittedPower_testing -= factor
      else:
        action = 1
        transmittedPower_testing += factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action
    
    # Resetting the attenuation to the begining
    self.setAttenuations(attenuation_dB = standardAttenuation)

    return transmittedPower_testing
  
  def plotDistance_ErrorProbability(self, **kwargs):
    """
    Plots a graph relating the distnace with the probability of error. All attenuations except loss attenuations must be added previous to this method

    Parameters:
    * transmittedPower -> The transmitted power by the transmitting station [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * standardDeviation_dB -> The standard deviation of the gaussian error that is in the attenuation of the channel [dB]
    * minDistance -> The stating distance for calculating the probability of error [m]
    * maxDistance -> The ending distance for calculating the probability of error [m]
    """
    transmittedPower = kwargs.get("transmittedPower", None)
    transmittedPower_dB = kwargs.get("transmittedPower_dB", None)
    if transmittedPower_dB == None and transmittedPower != None: transmittedPower_dB = utils.NaturalToLogarithmic(transmittedPower)
    elif transmittedPower_dB == None and transmittedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    elif sensitivity_dB == None and sensitivity == None: raise Exception("Sensitivity parameter is missing")

    standardDeviation_dB = kwargs.get("standardDeviation_dB", None)
    if standardDeviation_dB == None: raise Exception("Standard deviation parameter is missing")

    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    minDistance = kwargs.get("minDistance", 1)
    if minDistance == None: raise Exception("Minimun distance parameter is missing")
    elif minDistance <= 0: raise Exception("Minimun distance must be higher than 0")

    maxDistance = kwargs.get("maxDistance", 10000)
    if maxDistance == None: raise Exception("Maximun distance parameter is missing")

    distances = np.arange(minDistance, maxDistance, 0.1)

    standardAttenuation = self.totalAttenuation_dB

    pE = []

    for distance in distances:
        self.setAttenuations(attenuation_dB = standardAttenuation)
        self.addAttenuation(attenuation_dB = self.lossAttenuation(distance = distance, **kwargs))
        pE.append(self.calculateReachProbability(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, standardDeviation_dB = standardDeviation_dB))

    # Resetting the attenuation to the begining
    self.setAttenuations(attenuation_dB = standardAttenuation)

    plt.plot(distances, pE, 'b')
    plt.axis([minDistance, maxDistance, min(pE), max(pE)])
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Distance [m]')
    plt.ylabel('probability of error [%]')
    plt.grid(True)
    plt.title("Distance - Error probability")
  
  def plotDistance_ReceivedPower(self, **kwargs):
    """
    Plots a graph relating the distnace with the sensitivity. All attenuations except loss attenuations must be added previous to this method

    Parameters:
    * transmittedPower -> The transmitted power by the transmitting station [W] or [dB]
    * sensitivity -> The sensitivity the receptor has [W] or [dB]
    * minDistance -> The stating distance for calculating the probability of error [m]
    * maxDistance -> The ending distance for calculating the probability of error [m]
    * lossModel -> The model we want to use to calculate path loss attenuation {"friis", "hataUrban", "hataSuburban", "hataOpen"}
    * If friis:
      - wavelength -> The wavelength of the signal being transmitted [m]
      - n(?) -> Pathloss exponent [No units]
    
    * If hataUrban:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
      - correctionFactorApplied -> The antenna height correction factor used in the formula, options:
        - "Small-Medium city" -> Optimized for small or medium sized cities
        - "Large city" -> Optimized for large cities
    
    * If hataSuburban / hataOpen:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    """
    transmittedPower = kwargs.get("transmittedPower", None)
    transmittedPower_dB = kwargs.get("transmittedPower_dB", None)
    if transmittedPower_dB == None and transmittedPower != None: transmittedPower_dB = utils.NaturalToLogarithmic(transmittedPower)
    elif transmittedPower_dB == None and transmittedPower == None: raise Exception("Transmitted power parameter is missing")

    sensitivity = kwargs.get("sensitivity", None)
    sensitivity_dB = kwargs.get("sensitivity_dB", None)
    if sensitivity_dB == None and sensitivity != None: sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
    # We can afford to not have sensitivity included

    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    minDistance = kwargs.get("minDistance", 1)
    if minDistance == None: raise Exception("Minimun distance parameter is missing")
    elif minDistance <= 0: raise Exception("Minimun distance must be higher than 0")

    maxDistance = kwargs.get("maxDistance", 10000)
    if maxDistance == None: raise Exception("Maximun distance parameter is missing")

    distances = np.arange(minDistance, maxDistance, 0.1)

    standardAttenuation = self.totalAttenuation_dB

    receivedPowers = []
    ind = 0
    cmap = []
    for distance in distances:
        self.setAttenuations(attenuation_dB = standardAttenuation)
        self.addAttenuation(attenuation_dB = self.lossAttenuation(distance = distance, **kwargs))
        receivedPower = self.calculateRecivedPower(transmittedPower_dB = transmittedPower_dB)
        receivedPowers.append(receivedPower)
        if sensitivity_dB != None:
          if receivedPower > sensitivity_dB: cmap.append('g')
          else: cmap.append('r')
          ind += 1
    
    if sensitivity_dB == None: cmap = 'b'

    # Resetting the attenuation to the begining
    self.setAttenuations(attenuation_dB = standardAttenuation)

    plt.scatter(distances, receivedPowers, c=cmap, marker=",")
    plt.axis([minDistance, maxDistance, min(receivedPowers), max(receivedPowers)])
    plt.xscale('linear')
    plt.xscale('linear')
    plt.xlabel('Distance [m]')
    plt.ylabel('Received power [dB]')
    plt.grid(True)
    plt.title("Distance - Received Power")

  def plotLossAttenuation(self, **kwargs):
    """
    Plots the graph relating the distance and the loss atenuation, depending on the model.

    Parameters:
    * minDistance -> The stating distance for calculating the probability of error [m]
    * maxDistance -> The ending distance for calculating the probability of error [m]
    * lossModel -> The model we want to use to calculate path loss attenuation {"friis", "hataUrban", "hataSuburban", "hataOpen"}
    * If friis:
      - wavelength -> The wavelength of the signal being transmitted [m]
      - n(?) -> Pathloss exponent [No units]
    
    * If hataUrban:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
      - correctionFactorApplied -> The antenna height correction factor used in the formula, options:
        - "Small-Medium city" -> Optimized for small or medium sized cities
        - "Large city" -> Optimized for large cities
    
    * If hataSuburban / hataOpen:
      - baseHeight -> The height of the base estation antenna, recommended from 30 to 200m [m]
      - mobileHeight -> The height of the mobile station antenna, recommended from 1 to 10m [m]
      - frequency -> The frequency used in the transmission, recommended from 150 to 1500MHz [MHz]
    """

    minDistance = kwargs.get("minDistance", 1)
    if minDistance == None: raise Exception("Minimun distance parameter is missing")
    elif minDistance <= 0: raise Exception("Minimun distance must be higher than 0")

    maxDistance = kwargs.get("maxDistance", 10000)
    if maxDistance == None: raise Exception("Maximun distance parameter is missing")

    lossModel = kwargs.get("lossModel", None)
    if lossModel == None: raise Exception("Loss model parameter is missing")

    distances = np.arange(minDistance, maxDistance, 0.1)

    attenuations = []

    for distance in distances:
      attenuations.append(self.lossAttenuation(distance = distance, **kwargs))

    plt.plot(distances, attenuations, 'b')
    plt.axis([minDistance, maxDistance, min(attenuations), max(attenuations)])
    plt.xscale('log')
    plt.yscale('linear')
    plt.xlabel('Distances [m]')
    plt.ylabel('Linear attenuations [dB]')
    plt.grid(True)
    plt.title('Loss attenuation for the {}'.format(lossModel))
  
  def plotFresnelAttenuation(self, nMin = -5.0, nMax = 5.0):
    """
    Plots the graph relating the fresnel parameter and the diffraction attenuation.

    Parameters:
    * nMin -> The minimun fresnel parameter to plot
    * nMax -> The maximun fresnel parameter to plot
    """
    v = np.arange(nMin, nMax, 0.01)

    F = []

    for n in range(v.size):
        
        F.append(self.calculateDifractionAttenuation(v[n]))

    plt.plot(v, F, 'b')
    plt.axis([nMin, nMax, -5, max(F)+5])
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Fresnel Diffraction Parameter')
    plt.ylabel('Attenuation by diffraction [dB]')
    plt.grid(True)
    plt.title('Knife edge diffraction')