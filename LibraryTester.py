# Importing all installed libraries
import numpy as np
import itertools
import random
import scipy as sp
import scipy.stats as sps
# import bitarray  # IDKW but it does not allow me to instal it to my computer
import math
import komm
import matplotlib.pyplot as plt
import cmath
import time

# Importing all custom libraries
import utils
import Gaussian
import MarkovChain
import ChannelElement
import PowerElement
import ModulationElement

# Testing "Gaussian.py"
"""testGaussian = Gaussian.Gaussian(0, 2)
testGaussian.plotGaussian(0, 1)
print(testGaussian.probabilityNormalizedRange(-4, 2.6))
plt.show()"""



# Testing "MarkovChain.py"
"""gilbertModel = MarkovChain.MarkovChain(2)
# gilbertModel.estimateParametersGilbert(generateSequenceBits(0.3, 1000000))
gilbertModel.estimateParametersGilbert(np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]))

""
ba = bitarray.bitarray()
ba.frombytes('Hello, my name is Pasblo'.encode('utf-8'))
print(ba.tolist())
gilbertModel.estimateParametersGilbert(ba.tolist())
""

gilbertModel.printReleventData()
gilbertModel.simulateModel(50, 0)"""



# Testing "ChannelElement.py"
"""channel = ChannelElement.channelElement("AWGN")
channel.plotFresnelAttenuation(-4, 4)
plt.show()
#print(channel.friisAttenuation(100, wavelength = FrequencyToWavelength(900e6)))
print("{}".format(channel.calculateDistance_reachProbability(transmittedPower_dB = 0, reachProbability = 0.49, sensitivity_dB = -110, standardDeviation_dB = 3, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6))))
#print("{}".format(channel.calculateDistance_sensitivity(transmittedPower_dB = 0, sensitivity_dB = -110, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6))))
channel.plotDistance_ErrorProbability(transmittedPower_dB = 0, sensitivity_dB = -110, standardDeviation_dB = 3, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6), minDistance = 1, maxDistance = 20000)
plt.show()
channel.plotDistance_ReceivedPower(transmittedPower_dB = 0, sensitivity_dB = None, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6), minDistance = 1, maxDistance = 1000)
plt.show()"""



# Testing "PowerElement.py"
"""cable = PowerElement.powerElement(attenuation_dB = 2)
amp = PowerElement.powerElement(gain_dB = 10, figure = 3, previousElement = cable)
filter = PowerElement.powerElement(attenuation_dB = 1, previousElement = amp)

cable.printRelevantData(name = "cable")
print("\n")
amp.printRelevantData(name = "amp")
print("\n")
filter.printRelevantData(name = "filter")
print("\n")
filter.printEquivalentValues()"""



# Testing "ModulationElement.py"
"""testModulator = ModulationElement.modulationElement("PSK", 2)
testModulator2 = ModulationElement.modulationElement("PSK", 8)
testModulator3 = ModulationElement.modulationElement("PSK", 16)
testModulator.drawConstellation()
plt.show() # Not showing inside to be able to add stuff outside

testModulator.draw_BER_EbNo_curve(EbNo_dB_min = 0, EbNo_dB_max = 18, BER_min = 1e-8, color = 'b', titleEnabled = False)
testModulator2.draw_BER_EbNo_curve(EbNo_dB_min = 0, EbNo_dB_max = 18, BER_min = 1e-8, color = 'g', titleEnabled = False)
testModulator3.draw_BER_EbNo_curve(EbNo_dB_min = 0, EbNo_dB_max = 18, BER_min = 1e-8, color = 'r', titleEnabled = False)
#testModulator.draw_Pe_EbNo_curve()
#testModulator2.draw_BER_EbNo_curve()
plt.show() # Not showing inside to be able to add stuff outside
print(testModulator.get_EbNo_from_Pe(Pe = 1e-6))
testModulator.printReleventData("test modulator")
#print(testModulator.get_BER_from_EbNo(0))"""