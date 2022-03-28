"""
Author: Pablo Rivero Lazaro
NIA: 100429366
Date started: 1-12-2021
File version: 1.0
Version date: 7-12-2021

Description:
  This file contains a class for simulating a modulator or demodulator, depending on the analysis that needs
  to be performed it will support several types of modulations.

Acclarations:
  EbNo 
  EsNo = SNR = EbNo*m
"""

import numpy as np
import komm
import math
import ComsChannelsSim.utils as utils
import matplotlib.pyplot as plt

class modulationElement:
  def __init__(self, modulation, M = 0, **kwargs):
    """
    Parameters:
    * modulations supported:
      Digital modulations
      - PSK {BPSK, QPSK, DPSK, DQPSK, OQPSK} (Phase-shift keying)
      - FSK {AFSK, MFSK, DTMF} (Frequency-shift keying)
      - ASK (Amplitude-shift keying)
      - OOK (On-off keying)
      - QAM (Quadrature amplitude modulation)
      - CPM {MSK, GMSK, CPFSK, OFDM} (Continuous phase modulation)
      - OFDM {DMT} (Orthogonal frequency-division multiplexing)
      - SS {DSSS, CSS, FHSS} (Spread spectrum techniques)

      Analog-over-analog methods
      - PAM (Pulse-amplitude modulation)
      - PWM (Pulse-width modulation)
      - PFM (Pulse-frequency modulation)
      - PPM (Pulse-position modulation)

      Analog-over-digital methods
      - PCM {DPCM, ADPCM} (Pulse-code modulation)
      - DM or Δ-modulation {ΣΔ, CVSDM or ADM} (Delta modulation)
      - PDM (Pulse-density modulation)
      
    * M Number of symbols used in the transmission
    * kwargs
      - amplitude 
      - phase offset in radians
      - labeling
        * natural 
        * reflected (Gray code for 1D constellations, including complex)
        * reflected_2d (Gray code for 2D constellations)
    """
    if modulation == "BPSK":
      self.modulation = "PSK"
      self.M = 2
    elif modulation == "QPSK":
      self.modulation = "PSK"
      self.M = 4
    else:
      self.modulation = modulation
      self.M = M
    
    self.amplitude = kwargs.get("amplitude", 1.0)
    self.phase_offset = kwargs.get("phase_offset", 0.0)
    if self.modulation == "QAM":
      self.labeling = kwargs.get("labeling", "reflected_2d")
    else:
      self.labeling = kwargs.get("labeling", "reflected")
    
    if self.modulation == "PSK": self.model = komm.PSKModulation(self.M)
    elif self.modulation == "QAM": self.model = komm.QAModulation(self.M)
    elif self.modulation == "PAM": self.model = komm.PAModulation(self.M)
    else: raise Exception("Modulation is not supported")

    self.m = math.log(self.M, 2)
  
  def codify(self, bits, **kwargs):
    """
    Converts a sequence of bits to a sequence of symbols

    Parameters:
    * bits -> An array of bits
    * 
    """
    if self.modulation == "PAM":
      # Use gray_code() HERE
      pass

  
  def decodify(self, symbols):
    pass
  
  def decisor(self, sequenece):
    pass
  
  def calculateTimeRatePack(self, **kwargs):
    """
    Calculates the bit and symbol, times and rates

    Parameters:
    * symbolTime(?) -> Time that a symbol takes to be transmitted [s]
    * bitTime(?) -> Time that a bit takes to be transmitted [s]
    * symbolRate(?) -> Frequency that symbols are sent at [Bd]
    * bitRate(?) -> Frequency that bits are sent at [bits/s]

    Returns:
    * Dictionary:
      - symbolTime(?) -> Time that a symbol takes to be transmitted [s]
      - bitTime(?) -> Time that a bit takes to be transmitted [s]
      - symbolRate(?) -> Frequency that symbols are sent at [Bd]
      - bitRate(?) -> Frequency that bits are sent at [bits/s]
    """

    symbolTime = kwargs.get("symbolTime", None)
    bitTime = kwargs.get("bitTime", None)
    symbolRate = kwargs.get("symbolRate", None)
    bitRate = kwargs.get("bitRate", None)

    timeRatePack = {
      "Ts": kwargs.get("symbolTime", None),
      "Tb": kwargs.get("bitTime", None),
      "Rs": kwargs.get("symbolRate", None),
      "Rb": kwargs.get("bitRate", None)
    }

    if timeRatePack["Ts"] != None:
      timeRatePack["Tb"] = timeRatePack["Ts"] / self.m
      timeRatePack["Rs"] = 1 / timeRatePack["Ts"]
      timeRatePack["Rb"] = timeRatePack["Rs"] / self.m

    elif timeRatePack["Tb"] != None:
      timeRatePack["Ts"] = timeRatePack["Tb"] * self.m
      timeRatePack["Rs"] = 1 / timeRatePack["Ts"]
      timeRatePack["Rb"] = timeRatePack["Rs"] / self.m

    elif timeRatePack["Rs"] != None:
      timeRatePack["Ts"] = 1 / timeRatePack["Rs"]
      timeRatePack["Tb"] = timeRatePack["Ts"] / self.m
      timeRatePack["Rb"] = timeRatePack["Rs"] / self.m
    
    elif timeRatePack["Rb"] != None:
      timeRatePack["Ts"] = self.m / timeRatePack["Rb"]
      timeRatePack["Tb"] = 1 / timeRatePack["Rb"]
      timeRatePack["Rs"] = timeRatePack["Rb"] * self.m

    else: raise Exception("Parameters Ts, Tb, Rs or Rb missing")
    
    return timeRatePack
  
  def calculateBandwithPack(self, **kwargs):
    """
    Calculates all types of bandwiths knowing only one of them

    Parameters:
    * W(?) -> Bandwith [rad/s]
    * B(?) -> Bandwith [Hz]

    Returns:
    * Dictionary:
      - "W" -> Bandwith [rad/s]
      - "B" -> Bandwith [Hz]
    """

    # Parameter extraction
    bandwithPack = {
      "W": kwargs.get("W", None),
      "B": kwargs.get("B", None)
    }

    # Parameter adjusting
    if bandwithPack["W"] == None and bandwithPack["B"] != None: bandwithPack["W"] = 2*math.pi*bandwithPack["B"]
    elif bandwithPack["B"] == None and bandwithPack["W"] != None: bandwithPack["B"] = bandwithPack["W"]/2*math.pi
    else: raise Exception("Parameters W or B missing")

    return bandwithPack

  def get_Bandwith_from_TimeRates(self, **kwargs):
    """
    Returns the bandwth pack from any time or rate.

    Parameters:
    * symbolTime(?) -> Time that a symbol takes to be transmitted [s]
    * bitTime(?) -> Time that a bit takes to be transmitted [s]
    * symbolRate(?) -> Frequency that symbols are sent at [Bd]
    * bitRate(?) -> Frequency that bits are sent at [bits/s]

    Returns:
    * Dictionary:
      - "W" -> Bandwith [rad/s]
      - "B" -> Bandwith [Hz]
    """

    timeRatePack = self.calculateTimeRatePack(**kwargs)
    B = 1/timeRatePack["Ts"]
    return self.calculateBandwithPack(B = B)
  
  def get_No_from_EbNo(self, **kwargs):
    """
    Returns the noise power spectral density from Eb

    Parameters:
    * EbNo(?) -> Energy per bit to noise power spectral density ratio [bits/(s*Hz)]
    * EbNo_dB(?) -> Energy per bit to noise power spectral density ratio [dB]

    Returns:
    * No -> Noise power spectral density [W/Hz]
    """
    # Obtaining the signal to noise ratio
    EbNo = kwargs.get("EbNo", None)
    EbNo_dB = kwargs.get("EbNo_dB", None)
    
    if EbNo == None and EbNo_dB != None: EbNo = utils.LogarithmicToNatural(EbNo_dB)
    elif EbNo_dB == None and EbNo != None: EbNo_dB = utils.NaturalToLogarithmic(EbNo)
    else: raise Exception("Parameters EbNo or EbNo_dB missing")

    return self.model.energy_per_bit / utils.LogarithmicToNatural(EbNo_dB)
  
  def get_EbNo_from_SNR(self, **kwargs):
    """
    Calculates EbNo from the SNR

    Parameters:
    * SNR(?) -> Signal to noise ratio [No units]
    * SNR_dB(?) -> Signal to noise ratio [dB]

    Returns:
    * EbNo -> Energy per bit to noise power spectral density ratio [bits/(s*Hz)]
    """

    # Obtaining the signal to noise ratio
    SNR = kwargs.get("SNR", None)
    SNR_dB = kwargs.get("SNR_dB", None)
    
    if SNR == None and SNR_dB != None: SNR = utils.LogarithmicToNatural(SNR_dB)
    elif SNR_dB == None and SNR != None: SNR_dB = utils.NaturalToLogarithmic(SNR)
    else: raise Exception("Parameters SNR or SNR_dB missing")

    # Obtaining the other parameters
    """timeRatePack = self.calculateTimeRatePack(**kwargs)
    bandwithPack = self.calculateBandwithPack(**kwargs)"""

    return utils.LogarithmicToNatural(SNR_dB - math.log(self.m, 10)) #SNR*(bandwithPack["W"]/timeRatePack["Rb"]) # 4.101 from Sklar"""
  
  def get_SNR_from_EbNo(self, **kwargs):
    """
    Calculates SNR from EbNo

    Parameters:
    * EbNo(?) -> Energy per bit to noise power spectral density ratio [bits/(s*Hz)]
    * EbNo_dB(?) -> Energy per bit to noise power spectral density ratio [dB]

    Returns:
    * SNR -> Signal to noise ratio [No units]
    """

    # Obtaining the signal to noise ratio
    EbNo = kwargs.get("EbNo", None)
    EbNo_dB = kwargs.get("EbNo_dB", None)
    
    if EbNo == None and EbNo_dB != None: EbNo = utils.LogarithmicToNatural(EbNo_dB)
    elif EbNo_dB == None and EbNo != None: EbNo_dB = utils.NaturalToLogarithmic(EbNo)
    else: raise Exception("Parameters EbNo or EbNo_dB missing")

    # Obtaining the other parameters
    """timeRatePack = self.calculateTimeRatePack(**kwargs)
    bandwithPack = self.calculateBandwithPack(**kwargs)"""

    return utils.LogarithmicToNatural(EbNo_dB * math.log(self.m, 10)) # EbNo*(timeRatePack["Rb"]/bandwithPack["W"]) # 4.101 from Sklar
  
  def get_EsNo_from_EbNo(self, **kwargs):
    """
    Converts from EbNo to EsNo

    Parameters:
    * EbNo(?) -> Energy per bit to noise power spectral density ratio [bits/(s*Hz)]
    * EbNo_dB(?) -> Energy per bit to noise power spectral density ratio [dB]

    Returns:
    * EsNo -> Energy per symbol to noise power spectral density [bits/(s*Hz)]
    """

    # Obtaining EbNo
    EbNo = kwargs.get("EbNo", None)
    EbNo_dB = kwargs.get("EbNo_dB", None)
    
    if EbNo == None and EbNo_dB != None: EbNo = utils.LogarithmicToNatural(EbNo_dB)
    elif EbNo_dB == None and EbNo != None: EbNo_dB = utils.NaturalToLogarithmic(EbNo)
    else: raise Exception("Parameters EbNo or EbNo_dB missing")

    return utils.LogarithmicToNatural(EbNo_dB)*self.m
  
  def get_Pe_from_BER(self, BER):
    """
    Converts BER to Pe

    Paramaters:
    * BER -> Bit error rate [bit errors/s]

    Returns:
    * Pe -> Symbol error rate aka SER [symbol errors/s]
    """
    return BER*self.m
  
  def get_BER_from_Pe(self, Pe):
    """
    Converts Pe to BER

    Parameters:
    * Pe -> Symbol error rate aka SER [symbol errors/s]

    Returns:
    * BER -> Bit error rate [bit errors/s]
    """
    return Pe/self.m
  
  def get_BER_from_EbNo(self, **kwargs):
    """
    Calculates BER from EbNo. Analytical method supposes that AWGN channels are being used.

    Parameters:
    * EbNo(?) -> Energy per bit to noise power spectral density ratio [bits/(s*Hz)]
    * EbNo_dB(?) -> Energy per bit to noise power spectral density ratio [dB]
    * method -> Method to perform the calculations. Options: {simulated, analytically}

    Returns:
    * BER -> Bit error rate [bit errors/s]
    """

    # Obtaining EbNo
    EbNo = kwargs.get("EbNo", None)
    EbNo_dB = kwargs.get("EbNo_dB", None)
    
    if EbNo == None and EbNo_dB != None: EbNo = utils.LogarithmicToNatural(EbNo_dB)
    elif EbNo_dB == None and EbNo != None: EbNo_dB = utils.NaturalToLogarithmic(EbNo)
    else: raise Exception("Parameters EbNo or EbNo_dB missing")

    method = kwargs.get("method", "analytically")

    # Simulated method (Process N samples though a channel and calculate the number of errors obtained)
    if method == "simulated":
      N = 1000000

      B = utils.generateSequenceBits(0.5, int(N*self.m))
      A = self.model.modulate(B)
      print("Noise power: {}".format(self.get_No_from_EbNo(EbNo_dB)))
      if self.modulation == "PSK" or self.modulation == "QAM":
        AWGN_channel = ChannelElement.channelElement("AWGN", noisePower = self.get_No_from_EbNo(EbNo_dB), band = "PB")
      
      elif self.modulation == "PAM" or self.modulation == "ASK":
        AWGN_channel = ChannelElement.channelElement("AWGN", noisePower = self.get_No_from_EbNo(EbNo_dB), band = "BB")

      z = AWGN_channel.generateNoise(N)
      q = A + z
      B_r = self.model.demodulate(q)
      errors = (B != B_r).sum()
      BER = (1.0 * errors / N*self.m)
      print("Errors detected {}".format(errors))
    
    # Using analytical formulas (Only for AWGN channels)
    elif method == "analytically":
      if self.modulation == "PSK":
        Pe = 2*utils.Q(math.sqrt(2*self.get_EsNo_from_EbNo(EbNo_dB = EbNo_dB))*math.sin(math.pi/self.M)) # 4.105 from Sklar
      
      elif self.modulation == "DPSK":
        Pe = 2*utils.Q(math.sqrt(2*self.get_EsNo_from_EbNo(EbNo_dB = EbNo_dB))*math.sin(math.pi/(math.sqrt(2)*self.M))) # 4.106 from Sklar
      
      elif self.modulation == "FSK":
        Pe = (self.M-1)*utils.Q(math.sqrt(self.get_EsNo_from_EbNo(EbNo_dB = EbNo_dB))) # 4.107 from Sklar
      
      elif self.modulation == "QAM":
        Pe = 4*(1-1/math.sqrt(self.M))*utils.Q(math.sqrt((3*self.get_EsNo_from_EbNo(EbNo_dB = EbNo_dB))/(self.M-1)))-4*math.pow((1-1/math.sqrt(self.M)), 2)*math.pow(utils.Q(math.sqrt((3*self.get_EsNo_from_EbNo(EbNo_dB = EbNo_dB))/(self.M-1))), 2) # 3 from ISIT
      
      elif self.modulation == "PAM":
        Pe = (2*(self.M-1)/self.M)*utils.Q(math.sqrt((6*self.m/(math.pow(self.M, 2)-1))*EbNo)) # 8 from BER

      else: raise Exception("Modulation does not support this action")
      BER = self.get_BER_from_Pe(Pe)
    
    return BER
  
  def get_Pe_from_EbNo(self, **kwargs):
    """
    Calculates Pe from EbNo. Analytical method supposes that AWGN channels are being used.

    Parameters:
    * EbNo(?) -> Energy per bit to noise power spectral density ratio [bits/(s*Hz)]
    * EbNo_dB(?) -> Energy per bit to noise power spectral density ratio [dB]
    * method -> Method to perform the calculations. Options: {simulated, analytically}

    Returns:
    * Pe -> Symbol error rate aka SER [symbol errors/s]
    """
    return self.get_Pe_from_BER(self.get_BER_from_EbNo(**kwargs))
  
  def get_BER_from_SNR(self, **kwargs):
    """
    Calculates Pe from SNR. Analytical method supposes that AWGN channels are being used.

    Parameters:
    * SNR(?) -> Signal to noise ratio [No units]
    * SNR_dB(?) -> Signal to noise ratio [dB]
    * method -> Method to perform the calculations. Options: {simulated, analytically}

    Returns:
    * BER -> Bit error rate [bit errors/s]
    """
    return self.get_BER_from_EbNo(EbNo = self.get_EbNo_from_SNR(**kwargs), **kwargs)
  
  def get_Pe_from_SNR(self, **kwargs):
    """
    Calculates Pe from SNR. Analytical method supposes that AWGN channels are being used.

    Parameters:
    * SNR(?) -> Signal to noise ratio [No units]
    * SNR_dB(?) -> Signal to noise ratio [dB]
    * method -> Method to perform the calculations. Options: {simulated, analytically}

    Returns:
    * Pe -> Symbol error rate aka SER [symbol errors/s]
    """
    return self.get_Pe_from_BER(self.get_BER_from_EbNo(EbNo = self.get_EbNo_from_SNR(**kwargs), **kwargs))

  def get_SNR_from_Pe(self, **kwargs):

    Pe = kwargs.get("Pe", None)
    ndigits = kwargs.get("ndigits", 9)
    Pe_obatained = 0
    SNR_testing = 0
    factor = 1.0
    prev_action = 0 # 0 stands for EbNo inc, 1 stands for EbNo dec
    action = 0
    while round(Pe_obatained, ndigits) != round(Pe, ndigits):
      Pe_obatained = self.get_Pe_from_SNR(SNR_dB = SNR_testing, method = "analytically", **kwargs)

      if Pe_obatained > Pe:
        action = 0
        SNR_testing += factor
      else:
        action = 1
        SNR_testing -= factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action

    return SNR_testing
  
  def get_EbNo_from_Pe(self, **kwargs):
    """
    """
    Pe = kwargs.get("Pe", None)
    ndigits = kwargs.get("ndigits", 9)
    Pe_obatained = 0
    EbNo_testing = 0
    factor = 1.0
    prev_action = 0 # 0 stands for EbNo inc, 1 stands for EbNo dec
    action = 0
    while round(Pe_obatained, ndigits) != round(Pe, ndigits):
      Pe_obatained = self.get_Pe_from_EbNo(EbNo_dB = EbNo_testing)

      if Pe_obatained > Pe:
        action = 0
        EbNo_testing += factor
      else:
        action = 1
        EbNo_testing -= factor

      if action == 1 and prev_action == 0: factor /= 10.0
      prev_action = action

    return EbNo_testing
  
  def drawConstellation(self, annotate = True):
    """
    Draws the constellations of the modulation being used
    """

    pointConstellation = self.model.constellation

    # extract real part
    x = [symbol.real for symbol in pointConstellation]
    # extract imaginary part
    y = [symbol.imag for symbol in pointConstellation]

    if self.modulation == "PSK":
      constellationShape = plt.Circle((0, 0), self.amplitude, fill=False)
    else: constellationShape = None

    fig, ax = plt.subplots(figsize=(8,8))

    # Points plotting
    ax.scatter(x, y)

    # Encoding & codification anotations
    if annotate:
      encoding = range(self.M)
      codification = [self.model.symbols_to_bits([symbol]) for symbol in range(self.M)]
      for i in range(self.M):
        ax.annotate("a" + str(encoding[i]) + str(codification[encoding[i]][::-1]), (x[i], y[i]), color="#FF0000", fontsize=14)
    
    # Shape plotting
    if constellationShape != None: ax.add_patch(constellationShape)

    # x-y axis plotting
    utils.plotAxis(ax)
  
  def draw_BER_EbNo_curve(self, **kwargs):
    """
    Draws the curve that relates the BER and EbNo for this modulation. It will stop drawing
    when the limits provided are reached or when the BER drops to "0". This function does not
    draw the final plot to be able to append it to other graphs.

    Parameters:
    * EbNo_dB_min -> Minimun EbNo to test with [dB]
    * EbNo_dB_max -> Maximun EbNo to test with [dB]
    * BER_min -> Minimun BER to plot [bit errors/s]
    * color -> Color of the curve to plot, using the matplotlib standrad
    * titleEnabled -> If this function adds a title to the graph [Boolean]
    """

    # Unpacking the parameters
    EbNo_dB_min = kwargs.get("EbNo_dB_min", 0)
    EbNo_dB_max = kwargs.get("EbNo_dB_max", 18)
    BER_min = kwargs.get("BER_min", 1e-9)
    color = kwargs.get("color", 'k')
    titleEnabled = kwargs.get("titleEnabled", True)

    EbNo_dB = EbNo_dB_min
    ber_range = [1]
    i = 0
    while EbNo_dB >= EbNo_dB_min and EbNo_dB < EbNo_dB_max+1 and ber_range[i] > 0.0:
      ber_range.append(self.get_BER_from_EbNo(EbNo_dB = EbNo_dB, method = "analytically"))
      i += 1
      EbNo_dB += 1
    ber_range.pop(0)
    EbNo_dB_range = list(range(EbNo_dB_min, EbNo_dB))
    #print("BER: {}, EbNo: {}".format(ber_range, EbNo_dB_range))
    plt.plot(EbNo_dB_range, ber_range, color + 'o', EbNo_dB_range, ber_range, color)
    plt.axis([EbNo_dB_range[0], EbNo_dB_range[-1],  BER_min, 1])
    plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel('EbNo(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    if titleEnabled: plt.title("{}{} Modulation".format(self.M, self.modulation))
  
  def draw_Pe_EbNo_curve(self, **kwargs):

    # Unpacking the parameters
    EbNo_dB_min = kwargs.get("EbNo_dB_min", 0)
    EbNo_dB_max = kwargs.get("EbNo_dB_max", 18)
    Pe_min = kwargs.get("Pe_min", 1e-6)
    color = kwargs.get("color", 'k')
    titleEnabled = kwargs.get("titleEnabled", True)
    plot = kwargs.get("plt", plt)

    EbNo_dB = EbNo_dB_min
    pe_range = [1]
    i = 0
    while EbNo_dB >= EbNo_dB_min and EbNo_dB < EbNo_dB_max+1 and pe_range[i] > 0.0:
      pe_range.append(self.get_Pe_from_EbNo(EbNo_dB = EbNo_dB, method = "analytically"))
      i += 1
      EbNo_dB += 1
    pe_range.pop(0)
    EbNo_dB_range = list(range(EbNo_dB_min, EbNo_dB))
    #print("Pe: {}, EbNo: {}".format(pe_range, EbNo_dB_range))
    plot.plot(EbNo_dB_range, pe_range, color + 'o', EbNo_dB_range, pe_range, color)
    plot.axis([EbNo_dB_range[0], EbNo_dB_range[-1],  Pe_min, 1])
    plot.xscale('linear')
    plot.yscale('log')
    plot.xlabel('EbNo(dB)')
    plot.ylabel('Pe')
    plot.grid(True)
    if titleEnabled: plot.title("{}{} Modulation".format(self.M, self.modulation))

  def draw_BER_SNR_curve(self, **kwargs):
    # HERE (Same as below)
    pass

  def draw_Pe_SNR_curve(self, **kwargs):

    # Unpacking the parameters
    SNR_dB_min = kwargs.get("SNR_dB_min", 0)
    SNR_dB_max = kwargs.get("SNR_dB_max", 18)
    Pe_min = kwargs.get("Pe_min", 1e-6)
    color = kwargs.get("color", 'k')
    titleEnabled = kwargs.get("titleEnabled", True)

    SNR_dB = SNR_dB_min
    pe_range = [1]
    i = 0
    while SNR_dB >= SNR_dB_min and SNR_dB < SNR_dB_max+1 and pe_range[i] > 0.0:
      pe_range.append(self.get_Pe_from_SNR(SNR_dB = SNR_dB, method = "analytically", **kwargs))
      i += 1
      SNR_dB += 1
    pe_range.pop(0)
    SNR_dB_range = list(range(SNR_dB_min, SNR_dB))
    #print("Pe: {}, EbNo: {}".format(pe_range, SNR_dB_range))
    plt.plot(SNR_dB_range, pe_range, color + 'o', SNR_dB_range, pe_range, color)
    plt.axis([SNR_dB_range[0], SNR_dB_range[-1],  Pe_min, 1])
    plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel('EbNo(dB)')
    plt.ylabel('Pe')
    plt.grid(True)
    if titleEnabled: plt.title("{}{} Modulation".format(self.M, self.modulation))
  
  def printReleventData(self, name = None):
    if name != None: print("Information about {}".format(name))
    else: print("Information about modulation element")
    print("Modulation used: {}{}".format(self.M, self.modulation))
    print("Es: {}, Eb: {}".format(self.model.energy_per_symbol, self.model.energy_per_bit))