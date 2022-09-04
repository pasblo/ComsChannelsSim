"""
Author: Pablo Rivero Lazaro (Pasblo)
Contact: pasblo39@gmail.com
Version: 1.0
"""

import matplotlib.pyplot as plt
import math
import numpy as np

# Importing all custom libraries
import ComsChannelsSim
import ComsChannelsSim.utils as utils
import ComsChannelsSim.Gaussian as Gaussian
import ComsChannelsSim.MarkovChain as MarkovChain
import ComsChannelsSim.ChannelElement as ChannelElement
import ComsChannelsSim.PowerElement as PowerElement
import ComsChannelsSim.ModulationElement as ModulationElement
import ComsChannelsSim.ErrorSimulations as errorSim


# Testing "Gaussian.py"
print("\n\n###### GAUSSIAN TEST ######\n")
testGaussian = Gaussian.Gaussian(0, 2)
testGaussian.plotGaussian(0, 1)
print(testGaussian.probabilityNormalizedRange(-4, 2.6))
plt.show()


# Testing "ChannelElement.py"
print("\n\n###### CHANNEL ELEMENT TEST ######\n")
channel = ChannelElement.channelElement("AWGN")
#channel.plotFresnelAttenuation(-4, 4)
plt.show()
#print(channel.friisAttenuation(100, wavelength = FrequencyToWavelength(900e6)))
print("{}".format(channel.calculateDistance_reachProbability(transmittedPower_dB = 0, reachProbability = 0.49, sensitivity_dB = -110, standardDeviation_dB = 3, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6))))
#print("{}".format(channel.calculateDistance_sensitivity(transmittedPower_dB = 0, sensitivity_dB = -110, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6))))
channel.plotDistance_ErrorProbability(transmittedPower_dB = 0, sensitivity_dB = -110, standardDeviation_dB = 3, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6), minDistance = 1, maxDistance = 20000)
plt.show()
channel.plotDistance_ReceivedPower(transmittedPower_dB = 0, sensitivity_dB = None, lossModel = "friis", wavelength = utils.FrequencyToWavelength(900e6), minDistance = 1, maxDistance = 1000)
plt.show()


# Testing "PowerElement.py"
print("\n\n###### POWER ELEMENT TEST ######\n")
cable = PowerElement.powerElement(attenuation_dB = 2)
amp = PowerElement.powerElement(gain_dB = 10, figure = 3, previousElement = cable)
filter = PowerElement.powerElement(attenuation_dB = 1, previousElement = amp)

cable.printRelevantData(name = "cable")
print("\n")
amp.printRelevantData(name = "amp")
print("\n")
filter.printRelevantData(name = "filter")
print("\n")
filter.printEquivalentValues()


# Testing "ModulationElement.py"
print("\n\n###### MODULATION ELEMENT TEST ######\n")
testModulator = ModulationElement.modulationElement("PSK", 2)
testModulator2 = ModulationElement.modulationElement("PSK", 8)
testModulator3 = ModulationElement.modulationElement("PSK", 16)
testModulator2.drawConstellation()
plt.show() # Not showing inside to be able to add stuff outside

testModulator.draw_BER_EbNo_curve(EbNo_dB_min = 0, EbNo_dB_max = 18, BER_min = 1e-8, color = 'b', titleEnabled = False)
testModulator2.draw_BER_EbNo_curve(EbNo_dB_min = 0, EbNo_dB_max = 18, BER_min = 1e-8, color = 'g', titleEnabled = False)
testModulator3.draw_BER_EbNo_curve(EbNo_dB_min = 0, EbNo_dB_max = 18, BER_min = 1e-8, color = 'r', titleEnabled = False)
testModulator.draw_Pe_EbNo_curve()
testModulator2.draw_BER_EbNo_curve()
plt.show() # Not showing inside to be able to add stuff outside
print(testModulator.get_EbNo_from_Pe(Pe = 1e-6))
testModulator.printReleventData("test modulator")
print(testModulator.get_BER_from_EbNo(EbNo_dB = 0))



######## Problem 4 ########
# Data
Rb = 10e3 # bit/s
sensitivity_dB = utils.dBm_to_dB(-110) # In dB
M = 4
modulation = "QAM"
transmittedPower_dB = 0 # dB
antennaGain = 0 # dB
transmitterAntennaHeight = 5 # m
receiverAntennaHeight = 1.5 # m
carrierFrequency = 900e6 # Hz

channel = ChannelElement.channelElement("AWGN")

print("\n\n###### Problem 4.1 ######\n")

# Section 1 a) (#4#1a)
channel.setAttenuations(attenuation_dB = 0)
distanceReached = channel.calculateDistance_sensitivity(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, lossModel = "friis", wavelength = utils.FrequencyToWavelength(carrierFrequency), n = 2, ndigits = 6)
print("Distance reached: {:.2f}m".format(distanceReached))

# Section 1 b) (#4#1b)
channel.setAttenuations(attenuation_dB = 0)
distanceReached4 = channel.calculateDistance_sensitivity(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, lossModel = "friis", wavelength = utils.FrequencyToWavelength(carrierFrequency), n = 4, ndigits = 6)
channel.setAttenuations(attenuation_dB = 0)
distanceReached7 = channel.calculateDistance_sensitivity(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, lossModel = "friis", wavelength = utils.FrequencyToWavelength(carrierFrequency), n = 7, ndigits = 6)
print("Distance reached: {:.2f}m (n = 4), {:.2f}m (n = 7)".format(distanceReached4, distanceReached7))

# Section 1 c) (#4#1c)
channel.setAttenuations(attenuation_dB = 0)
distanceReached = channel.calculateDistance_sensitivity(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, lossModel = "hataUrban", baseHeight = transmitterAntennaHeight, mobileHeight = receiverAntennaHeight, frequency = carrierFrequency/1e6, correctionFactorApplied = "Small-Medium city", ndigits = 6)
print("Distance reached: {:.2f}m".format(distanceReached))

# Section 1 d) (#4#1b)
channel.setAttenuations(attenuation_dB = 5e-2)
distanceReached = channel.calculateDistance_sensitivity(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = sensitivity_dB, lossModel = "friis", wavelength = utils.FrequencyToWavelength(carrierFrequency), n = 4, ndigits = 6)
print("Distance reached: {:.2f}m".format(distanceReached))


######## Problem 5 ########
# Data
distance = 35786 # Km
ch1_freq = 8e9 # Hz
ch1_band = 1e6 # Hz
ch1_att = 1e-2 # dB/Km
ch2_freq = 26e9 # Hz
ch2_band = 10e6 # Hz
ch2_att = 1.4e-1 # dB/Km

antenna_gain_dB = 60 # dB
antenna_temp = 50 # K

cable_attenuationMeter = 10/1000.0 # dB/m
cable_length = 10 # m

amp_gain_dB = 40 # dB
amp_figure = 20 # dB

# Section 1
print("\n\n###### Problem 5.1 ######\n")
sateliteAntennaGain_dB = 10 # dB
Pe_objective = 1e-6

# Calculate SNR (Supposing 4-QAM) (Undestanding Pe as SER)
demodulator = ModulationElement.modulationElement("QAM", M = 4)
SNR_dB = demodulator.get_SNR_from_Pe(Pe = Pe_objective)
print("SNR obtained: {:.2f}dB".format(SNR_dB))

# Calculate sensitivity
cable = PowerElement.powerElement(attenuationDistance_dB = cable_attenuationMeter, distance = cable_length)
cable.printRelevantData()
amp = PowerElement.powerElement(gain_dB = amp_gain_dB, figure = amp_figure, previousElement = cable)
amp.printRelevantData()
totalTemperature = amp.calculateEquivalentTemperature() + antenna_temp
print("Total temperature: {:.2f}K".format(totalTemperature))

sensitivity = utils.calculateSensitivity(SNR_dB = SNR_dB, equivalentTemperature = totalTemperature, bandwith = ch1_band)
sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
print("Sensitivity required: {:.2f}dB".format(sensitivity_dB))

# Add attenuations and gains
channel1 = ChannelElement.channelElement("AWGN")
channel1.addGain(gain_dB = sateliteAntennaGain_dB) # Satelite antenna
channel1.addGain(gain_dB = antenna_gain_dB) # Ground station antenna
channel1.addAttenuation(attenuation_dB = 480*ch1_att) # Attenuation of the medium
channel1.addAttenuation(attenuation_dB = channel1.lossAttenuation(distance = distance, lossModel = "friis", wavelength = utils.FrequencyToWavelength(ch1_freq)))
channel1.addGain(gain_dB = amp.calculateEquivalentGain()) # Amplification stage

# Calculate transmitted power
transmittedPowerNeeded_dB = channel1.calculateTransmittedPower(receivedPower_dB = sensitivity_dB)
print("Transmitted power needed: {:.2f}dB".format(transmittedPowerNeeded_dB))

# Section 2
print("\n\n###### Problem 5.2 ######\n")
# Calculating the necesary received power to ensure a disponibility of 98%
receivedPower_dB = channel1.calculateReceivedPower_disponibility(disponibility_objetive = 0.98, sensitivity_dB = sensitivity_dB, standardDeviation = 3.5)
print("Received power needed: {:.2f}dB".format(receivedPower_dB))

linkMargin = channel1.calculateLinkMargin(receivedPower_dB = receivedPower_dB, sensitivity_dB = sensitivity_dB)
print("Link margin: {:.2f}dB".format(linkMargin))

# Section 3
print("\n\n###### Problem 5.3 ######\n")
newSensitivity_dB = sensitivity_dB + linkMargin

testing_amp = amp_gain_dB

factor = 1.0
transmittedPower_dB = -1
prev_action = 0 # 0 stands for distance inc, 1 stands for distance dec
action = 0
ndigits = 6
while round(transmittedPower_dB, ndigits) != round(transmittedPowerNeeded_dB, ndigits):
	channel1.setGains()
	channel1.setAttenuations()
	channel1.addGain(gain_dB = sateliteAntennaGain_dB) # Satelite antenna
	channel1.addGain(gain_dB = antenna_gain_dB) # Ground station antenna
	channel1.addAttenuation(attenuation_dB = 480*ch1_att) # Attenuation of the medium
	amp = PowerElement.powerElement(gain_dB = testing_amp, figure = amp_figure, previousElement = cable)
	channel1.addGain(gain_dB = amp.calculateEquivalentGain()) # Amplification stage
	transmittedPower_dB = channel1.calculateTransmittedPower(receivedPower_dB = newSensitivity_dB)
	# print("For gain {:.2f}dB, we have transmittedPower {:.2f}dB, with gain {:.2f}dB".format(testing_amp, transmittedPower_dB, amp.calculateEquivalentGain()))

	# Calculating the new distance
	if transmittedPower_dB > transmittedPowerNeeded_dB:
		action = 0
		testing_amp += factor

	else:
		action = 1
		testing_amp -= factor

	if action == 1 and prev_action == 0: factor /= 10.0
	prev_action = action

print("Amplification gain: {:.2f}dB".format(testing_amp))

# Section 4
print("\n\n###### Problem 5.4 ######\n")
# The bandwith changes -> SNR changes -> SNR is directly proportional to Rb
testing_amp = amp_gain_dB

factor = 1.0
SNR_testing_dB = 1
prev_action = 0 # 0 stands for distance inc, 1 stands for distance dec
action = 0
ndigits = 6
while round(sensitivity_dB, ndigits) != round(newSensitivity_dB, ndigits):
	sensitivity = utils.calculateSensitivity(SNR_dB = SNR_testing_dB, equivalentTemperature = totalTemperature, bandwith = ch1_band)
	sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
	# print("For SNR {:.2f}dB, we have sensitivity {:.2f}dB".format(SNR_testing_dB, sensitivity_dB))

	# Calculating the new distance
	if sensitivity_dB < newSensitivity_dB:
		action = 0
		SNR_testing_dB += factor

	else:
		action = 1
		SNR_testing_dB -= factor

	if action == 1 and prev_action == 0: factor /= 10.0
	prev_action = action

print("New SNR: {:.2f}dB".format(SNR_testing_dB))
print("Compression factor: {:.2f}:1".format(SNR_testing_dB/SNR_dB))


######## Problem 15 ########

# Data
sound_speed = 1500 # m/s
distance = 50 #m
Rs = 2400 #symb/s
modulation = "BPSK"
n = 31 #Symbols

# State 0 -> Good, state 1 -> Bad
gilbert_Pe_bad = 0.3
gilbert_t00 = 0.99 # Remember that we have the order reversed in simulation
gilbert_t11 = 0.88 

# Section 1 (#15#1)
print("\n\n###### Problem 15.1 ######\n")
gilbert_transition = [[gilbert_t00, 1 - gilbert_t11], [1 - gilbert_t00, gilbert_t11]]
gilbert_errorProbabilities = [0, gilbert_Pe_bad]
markov = MarkovChain.markovChain(M = 2, T = gilbert_transition, Pe = gilbert_errorProbabilities)
markov.printReleventData()

# Section 2 (#15#2)
print("\n\n###### Problem 15.2 ######\n")
dopler = markov.getT(1, 0)*Rs*markov.getΠ(1)
print("\nDopler: {:.2f}".format(dopler))
Tc = 1/dopler
print("Tc: {:.4f}sec".format(Tc))
capacity = Tc*Rs
print("Capacity of the channel: {:.2f}symb/Tc, ".format(capacity))

bad_average_symb = capacity*markov.getΠ(1)
print("Bad average transmitted symbols: {:.2f}symb".format(bad_average_symb))
good_average_symb = capacity*markov.getΠ(0)
print("Good average transmitted symbols: {:.2f}symb".format(good_average_symb))

# Checking if the simulation is correct
errorSequence = markov.simulateModel(100000, 0)
errorProbability = errorSim.estimateErrorProbability(np.array([1]), errorSequence)
print("\nSimulated error probability: {}\n".format(errorProbability))