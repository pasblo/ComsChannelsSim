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

######## Problem 1 ########

# Seccion 2
modulator1 = ModulationElement.modulationElement("QPSK")
modulator2 = ModulationElement.modulationElement("PSK", 8)

print("QPSK EbNo {}dB".format(modulator1.get_EbNo_from_Pe(Pe = 1e-4)))
print("8-PSK EbNo {}dB".format(modulator2.get_EbNo_from_Pe(Pe = 1e-4)))
modulator1.draw_Pe_EbNo_curve(color = 'b', titleEnabled = False)
modulator2.draw_Pe_EbNo_curve(color = 'r', titleEnabled = False)
plt.title("QPSK vs 8-PSK modulations")
plt.show()


# Section 3
modulator3 = ModulationElement.modulationElement("PSK", 8)
bandwithPack = modulator3.get_Bandwith_from_TimeRates(bitRate = 72000)
print("Bandwith: {}Hz".format(bandwithPack["B"]))

wavelength = utils.FrequencyToWavelength(40000, speed = 1435)
print("Wavelength: {}m".format(wavelength))


# Section 5
modulator3 = ModulationElement.modulationElement("PSK", 8)
SNR_dB = modulator3.get_SNR_from_Pe(Pe = 1e-4)
print("SNR: {:.2f}dB".format(SNR_dB))

sensitivity = utils.calculateSensitivity(SNR = utils.LogarithmicToNatural(SNR_dB), bandwith = 24000, equivalentTemperature = 10000)
sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
print("Sensitivity: {:.2f}dB".format(sensitivity_dB))


# Section 6
channel = ChannelElement.channelElement("AWGN")
receivedPower_dB = channel.calculateReceivedPower_disponibility(disponibility_objetive = 0.98, sensitivity_dB = sensitivity_dB, standardDeviation = 3)
linkMargin = channel.calculateLinkMargin(receivedPower_dB = receivedPower_dB, sensitivity_dB = sensitivity_dB)
print("Link margin: {:.2f}dB".format(linkMargin))

new_sensitivity_dB = sensitivity_dB + linkMargin
print("New sensitivity: {:.2f}dB".format(new_sensitivity_dB))


# Section 7
def calculateTotalTemperature(LNA_gain):
	BPF1 = PowerElement.powerElement(attenuation_dB = 5)
	LNA = PowerElement.powerElement(gain_dB = LNA_gain, figure = 0.9, previousElement = BPF1)
	BPF2 = PowerElement.powerElement(attenuation_dB = 5, previousElement = LNA)
	mixer = PowerElement.powerElement(attenuation_dB = 10, previousElement = BPF2)
	BPF3 = PowerElement.powerElement(attenuation_dB = 5, previousElement = mixer)
	#BPF3.printEquivalentValues()
	return BPF3.calculateEquivalentTemperature()

minTemp = calculateTotalTemperature(17.5)
maxTemp = calculateTotalTemperature(15.5)
typTemp = calculateTotalTemperature(16.5)
print("Total system temperature: {:.2f}K - {:.2f}K, typ: {:.2f}".format(minTemp, maxTemp, typTemp))

minAntennaTemp = 103
minAntennaTempVar = minAntennaTemp*3/2

minTempJointLow = minTemp + minAntennaTemp
minTempJointTyp = typTemp + minAntennaTemp
minTempJointHigh = maxTemp + minAntennaTemp

minTempJointLowVar = minTemp + minAntennaTempVar
minTempJointTypVar = typTemp + minAntennaTempVar
minTempJointHighVar = maxTemp + minAntennaTempVar
print("Total min temperature variation: {:.2f}% - {:.2f}%, typ: {:.2f}%".format(100*(1-minTempJointLow/minTempJointLowVar), 100*(1-minTempJointHigh/minTempJointHighVar), 100*(1-minTempJointTyp/minTempJointTypVar)))


maxAntennaTemp = 396
maxAntennaTempVar = maxAntennaTemp*3/2

maxTempJointLow = minTemp + maxAntennaTemp
maxTempJointTyp = typTemp + maxAntennaTemp
maxTempJointHigh = maxTemp + maxAntennaTemp

maxTempJointLowVar = minTemp + maxAntennaTempVar
maxTempJointTypVar = typTemp + maxAntennaTempVar
maxTempJointHighVar = maxTemp + maxAntennaTempVar
print("Total max temperature variation: {:.2f}% - {:.2f}%, typ: {:.2f}%".format(100*(1-maxTempJointLow/maxTempJointLowVar), 100*(1-maxTempJointHigh/maxTempJointHighVar), 100*(1-maxTempJointTyp/maxTempJointTypVar)))


# Section 8
sensor = PowerElement.powerElement(attenuation_dB = 0, temperature = 10000)
satelite = PowerElement.powerElement(gain_dB = 30, temperature = 950, previousElement = sensor)

print("Total temperature: {:.2f}K".format(satelite.calculateEquivalentTemperature()))


# Section 9
modulator4 = ModulationElement.modulationElement("PSK", 8)
SNR_dB4 = modulator4.get_SNR_from_Pe(Pe = 1e-4)
print("SNR: {:.2f}dB".format(SNR_dB4))

signalPower = utils.calculateSensitivity(SNR_dB = SNR_dB4, equivalentTemperature = 10950, bandwith = 24000)
print("Signal power: {:.2f}dB".format(utils.NaturalToLogarithmic(signalPower)))



######## Problem 2 ########

# Section 1
antenna = PowerElement.powerElement(gain_dB = 0, temperature = 300)
cable = PowerElement.powerElement(attenuation_dB = 2, previousElement = antenna)
amp = PowerElement.powerElement(gain_dB = 10, figure = 3, previousElement = cable)
filter = PowerElement.powerElement(attenuation_dB = 1, previousElement = amp)
temperature = filter.calculateEquivalentTemperature()
print("System temperature: {:.2f}K".format(temperature))

# Section 4 REDO with tip-ex
modulator5 = ModulationElement.modulationElement("QPSK")
SNR_dB = modulator5.get_SNR_from_Pe(Pe = 1e-6)
print("SNR: {:.2f}dB".format(SNR_dB))

# Section 5
sensitivity = utils.calculateSensitivity(SNR = utils.LogarithmicToNatural(SNR_dB), equivalentTemperature = temperature, bandwith = 33000)
print("Sensitivity: {:.2f}dB".format(utils.NaturalToLogarithmic(sensitivity)))

# Section 6
channel2 = ChannelElement.channelElement("AWGN")
lossAttenuation = channel2.lossAttenuation(distance = 10000, lossModel = "friis", wavelength = utils.FrequencyToWavelength(300e6), n = 2.5)
print("Attenuation by propagation: {:.2f}dB".format(lossAttenuation))

modulator5 = ModulationElement.modulationElement("QPSK")
SNR_dB = modulator5.get_SNR_from_Pe(Pe = 1e-6)
print("SNR: {:.2f}dB".format(SNR_dB))

sensitivity = utils.calculateSensitivity(SNR = utils.LogarithmicToNatural(SNR_dB), equivalentTemperature = temperature, bandwith = 300000)
sensitivity_dB = utils.NaturalToLogarithmic(sensitivity)
print("Sensitivity: {:.2f}dB".format(sensitivity_dB))

transmittedPower_dBm = utils.dB_to_dBm(sensitivity_dB + lossAttenuation)
print("Minimun transmitted power needed: {:.2f}dBm".format(transmittedPower_dBm))

# Section 7
channel3 = ChannelElement.channelElement("AWGN")
lossAttenuation = channel2.lossAttenuation(distance = 10000, lossModel = "friis", wavelength = utils.FrequencyToWavelength(300e6), n = 2.5)
print("Attenuation by propagation: {:.2f}dB".format(lossAttenuation))

modulator5 = ModulationElement.modulationElement("QPSK")
SNR_dB = modulator5.get_SNR_from_Pe(Pe = 1e-6)
print("SNR: {:.2f}dB".format(SNR_dB))

sensitivity = utils.calculateSensitivity(SNR = utils.LogarithmicToNatural(SNR_dB), equivalentTemperature = temperature, bandwith = 27270)
sensitivity2_dB = utils.NaturalToLogarithmic(sensitivity)
print("Sensitivity: {:.2f}dB".format(utils.NaturalToLogarithmic(sensitivity)))

transmittedPower_dBm = utils.dB_to_dBm(sensitivity2_dB + lossAttenuation)
print("Minimun transmitted power needed: {:.2f}dBm".format(transmittedPower_dBm))

# Section 8
channel4 = ChannelElement.channelElement("AWGN")
transmittedPower_dB = channel4.calculatePower_reachProbability(distance = 10000, sensitivity_dB = sensitivity_dB, standardDeviation_dB = 4.5, lossModel = "friis", wavelength = utils.FrequencyToWavelength(300e6), n = 2.5, reachProbability = 0.1)
print("Tranmistted power needed: {:.2f}dBm".format(utils.dB_to_dBm(transmittedPower_dB)))

channel5 = ChannelElement.channelElement("AWGN")
receivedPower_dB = channel5.calculateReceivedPower_disponibility(disponibility_objetive = 0.9, sensitivity_dB = sensitivity_dB, standardDeviation = 4.5)
print("Received power: {:.2f}dB".format(receivedPower_dB))
linkMargin = channel5.calculateLinkMargin(receivedPower_dB = receivedPower_dB, sensitivity_dB = sensitivity_dB)
print("Link margin: {:.2f}dB".format(linkMargin))
new_sensitivity_dB = sensitivity_dB + linkMargin

print("New transmitted power needed: {:.2f}dBm".format(utils.dB_to_dBm(new_sensitivity_dB + lossAttenuation)))

# Section 9
channel5 = ChannelElement.channelElement("AWGN")
receivedPower_dB = channel5.calculateReceivedPower_disponibility(disponibility_objetive = 0.9, sensitivity_dB = sensitivity_dB, standardDeviation = 4.5)
print("Received power: {:.2f}dB".format(receivedPower_dB))
distance = channel5.calculateDistance_attenuation(attenuation_objetive = -(receivedPower_dB + linkMargin), lossModel = "friis", wavelength = utils.FrequencyToWavelength(300e6), n = 2.5)
print("Distance: {:.2f}m".format(distance))



######## Problem 3 ########

# Section 1 (No hemos añadido la antena, dejar claro)
antenna = PowerElement.powerElement(temperature = 290, gain_dB = 60)
amp = PowerElement.powerElement(gain_dB = 16.5, figure = 0.9)
amp.printRelevantData()
cable = PowerElement.powerElement(attenuationDistance_dB = 1.8/1000.0, distance = 500, previousElement = amp)
cable.printRelevantData()
equivalentAttenuation = -cable.calculateEquivalentGain()
print("Equivalent attenuation: {:.2f}dB".format(equivalentAttenuation))

# Section 2
equivalentTemperature = amp.calculateEquivalentTemperature()
systemTemperature = equivalentTemperature + 290
print("System temperature: {:.2f}K".format(systemTemperature))

# Section 3
demodulator = ModulationElement.modulationElement("QAM", M = 4)
SNR_dB = demodulator.get_SNR_from_Pe(Pe = 10e-5)
print("SNR: {:.2f}dB".format(SNR_dB))

# Section 4



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

# Section 2 (#4#2)
receivedPower_dB = channel.calculateReceivedPower_disponibility(disponibility_objetive = 0.95, sensitivity_dB = sensitivity_dB, standardDeviation = 3)
linkMargin = channel.calculateLinkMargin(receivedPower_dB = receivedPower_dB, sensitivity_dB = sensitivity_dB)
print("Link margin: {:.2f}dB".format(linkMargin))

# Section 3 (#4#3)
newSensitivity_dB = sensitivity_dB + linkMargin # Adding the link margin to the sensitivity to take it into account (Maybe is -)
distanceReached = channel.calculateDistance_sensitivity(transmittedPower_dB = transmittedPower_dB, sensitivity_dB = newSensitivity_dB, lossModel = "hataUrban", baseHeight = transmitterAntennaHeight, mobileHeight = receiverAntennaHeight, frequency = carrierFrequency/1e6, correctionFactorApplied = "Small-Medium city", ndigits = 6)
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
# Calculating the necesary received power to ensure a disponibility of 98%
receivedPower_dB = channel1.calculateReceivedPower_disponibility(disponibility_objetive = 0.98, sensitivity_dB = sensitivity_dB, standardDeviation = 3.5)
print("Received power needed: {:.2f}dB".format(receivedPower_dB))

linkMargin = channel1.calculateLinkMargin(receivedPower_dB = receivedPower_dB, sensitivity_dB = sensitivity_dB)
print("Link margin: {:.2f}dB".format(linkMargin))

# Section 3
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

# Section 5

# Section 6
fiber_distance = 10 # Km
fiber_att = 0.1 # dB/Km

rx_sensitivity_dB = -40 # dB

Rb_ref = 2e9 # bps
Pe = 1e-7
diode_spectral = 2e-9 # m

channel2 = ChannelElement.channelElement("AWGN")
channel2.addAttenuation(attenuation_dB = fiber_att*fiber_distance)
transmittedPower_dB = channel2.calculateTransmittedPower(receivedPower_dB = rx_sensitivity_dB)
transmittedPower = utils.LogarithmicToNatural(utils.dB_to_dBm(transmittedPower_dB))
print("Minimun transmitted power: {:.2f}mW".format(transmittedPower))

# Section 7



######## Problem 6 ########

# Data
link1_modulation = "QAM"
link1_modulation_M = 64
link1_modulator_Rs = 15e6 # Symbols / s

link1_link_freq = 14e9 # Hz

link1_tx_power = 0.5 # W
link1_tx_power_dB = utils.NaturalToLogarithmic(link1_tx_power) # dB
link1_tx_antenna_gain_dB = 28 # dB

link1_tx_rx_distance = 50e3 # m
link1_tx_vano_distance = 10e3 # m
link1_rx_vano_distance = link1_tx_rx_distance - link1_tx_vano_distance # m
link1_vano_height = 10 # m
link1_link_margin = 6 # dB

link1_rx_antenna_gain_dB = 28 # dB
link1_rx_LNA_gain_dB = 25 # dB
link1_rx_LNA_figure = 2 # dB
link1_rx_line_attenuation_dB = 2 # dB
link1_rx_amp_gain_dB = 30 # dB
link1_rx_amp_figure = 15 # dB
link1_rx_dem_sensitivity_dB = utils.dBm_to_dB(-90) # dB

link2_modulation = "QPSK"
link2_modulation_Rs = 15e6 # Symbols / s

link2_asc_freq = 14e9 # Hz

link2_asc_distance = 36000 # Km
link2_asc_att = 2e-2 # dB/Km
link2_asc_attenuations = 6 # dB
link2_asc_link_margin = 4 # dB

link2_asc_tx_power = 100 # W
link2_asc_tx_power_dB = utils.NaturalToLogarithmic(link2_asc_tx_power)
link2_asc_tx_antenna_gain_dB = 40 # dB

link2_asc_rx_antenna_gain_dB = 40 # dB
link2_asc_rx_figure = 4 # dB
link2_asc_rx_sensibility_dB = utils.dBm_to_dB(-90) # dB

link2_desc_freq = 12e9 # Hz

link2_desc_distance = 36000 # Km
link2_desc_att = 1.2e-2 # dB/Km

link2_desc_tx_power = 30 # W
link2_desc_tx_power_dB = utils.NaturalToLogarithmic(link2_desc_tx_power) # dB
link2_desc_tx_antenna_gain_dB = 45 # dB

link2_desc_atenuations = 4 # dB
link2_desc_link_margin = 6 # dB

link2_desc_rx_antenna_gain_dB = 45 # dB
link2_desc_rx_antenna_temp = 200 # K
link2_desc_rx_LNA_gain_dB = 30 # dB
link2_desc_rx_LNA_figure = 3 # dB
link2_desc_rx_line_attenuation_dB = 2 # dB
link2_desc_rx_amp_gain_dB = 20 # dB
link2_desc_rx_amp_figure = 20 # dB
link2_desc_rx_dem_sensitivity_dB = utils.dBm_to_dB(-90)

# Section 1 (Inconcluso)
# For calculating Pe, we need SNR
# For SNR we need Ps and Pn
# For Ps we need all attenuations and gains from the line
# For Pn we need the equivalent temperature from the receptor and the bandwith

# Calculating the equivalent temperature of the link1
LNA = PowerElement.powerElement(gain_dB = link1_rx_LNA_gain_dB, figure = link1_rx_LNA_figure)
line = PowerElement.powerElement(attenuation_dB = link1_rx_line_attenuation_dB, previousElement = LNA)
amp = PowerElement.powerElement(gain_dB = link1_rx_amp_gain_dB, figure = link1_rx_amp_figure, previousElement = line)
totalTemperature = amp.calculateEquivalentTemperature()
print("Equivalent temperature link 1 receptor: {:.2f}K".format(totalTemperature))

# Calculating the bandwith of the link1
link1_demodulator = ModulationElement.modulationElement(link1_modulation, link1_modulation_M)
link1_bandwith = link1_demodulator.get_Bandwith_from_TimeRates(symbolRate = link1_modulator_Rs)["B"]
print("Link 1 bandwith: {:.2f}Hz".format(link1_bandwith))

# Calculating the noise power
noisePower = utils.claculateNoisePower(equivalentTemperature = totalTemperature, bandwith = link1_bandwith)
noisePower_dB = utils.NaturalToLogarithmic(noisePower)
print("Noise power: {:.2f}dB".format(noisePower_dB))

# Calculating the received power
link1_channel = ChannelElement.channelElement("AWGN")
link1_channel.addGain(gain_dB = link1_tx_antenna_gain_dB)
link1_channel.addAttenuation(attenuation_dB = link1_channel.diffractionAttenuation(tx_distance = link1_tx_vano_distance, rx_distance = link1_rx_vano_distance, distance_to_peak = link1_vano_height, wavelength = utils.FrequencyToWavelength(link1_link_freq)))
link1_channel.addAttenuation(attenuation_dB = link1_channel.lossAttenuation(distance = link1_tx_rx_distance, lossModel = "friis", wavelength = utils.FrequencyToWavelength(link1_link_freq)))
link1_channel.addGain(gain_dB = link1_rx_antenna_gain_dB)
link1_channel.addAttenuation(attenuation_dB = link1_link_margin) # Adding the link margin so we take it into account

signalPower_dB = link1_channel.calculateRecivedPower(transmittedPower_dB = link1_tx_power_dB)
print("Signal power: {:.2f}dB".format(signalPower_dB))

SNR_dB = signalPower_dB - noisePower_dB
print("SNR obtained: {:.2f}dB".format(SNR_dB))

#link1_demodulator.draw_Pe_SNR_curve(SNR_dB_max = 50)
#plt.show()
link1_Pe = link1_demodulator.get_Pe_from_SNR(SNR_dB = SNR_dB)
print("Pe obtained: {}".format(link1_Pe))

print("\n")

# Section 2
# Calculating the equivalent temperature of the link2 asc
receptor = PowerElement.powerElement(gain_dB = 0, figure = link2_asc_rx_figure)
totalTemperature = receptor.calculateEquivalentTemperature()

# Calculating the bandwith of the link2
link2_demodulator = ModulationElement.modulationElement(link2_modulation)
link2_bandwith = link2_demodulator.get_Bandwith_from_TimeRates(symbolRate = link2_modulation_Rs)["B"]
print("Link 2 bandwith: {:.2f}Hz".format(link2_bandwith))

# Calculating the noise power asc
noisePowerAsc = utils.claculateNoisePower(equivalentTemperature = totalTemperature, bandwith = link2_bandwith)
noisePowerAsc_dB = utils.NaturalToLogarithmic(noisePowerAsc)
print("Noise power asc: {:.2f}dB".format(noisePowerAsc_dB))

# Calculating the equivalent temperature of the link2 desc
LNA = PowerElement.powerElement(gain_dB = link2_desc_rx_LNA_gain_dB, figure = link2_desc_rx_LNA_figure)
line = PowerElement.powerElement(attenuation_dB = link2_desc_rx_line_attenuation_dB, previousElement = LNA)
amp = PowerElement.powerElement(gain_dB = link2_desc_rx_amp_gain_dB, figure = link2_desc_rx_amp_figure, previousElement = line)
totalTemperature = amp.calculateEquivalentTemperature()
print("Equivalent temperature link 2 receptor: {:.2f}K".format(totalTemperature))

# Calculating the noise power desc
noisePowerDesc = utils.claculateNoisePower(equivalentTemperature = totalTemperature, bandwith = link2_bandwith)
noisePowerDesc_dB = utils.NaturalToLogarithmic(noisePowerDesc)
print("Noise power desc: {:.2f}dB".format(noisePowerDesc_dB))

totalNoisePower_dB = utils.NaturalToLogarithmic(noisePowerAsc + noisePowerDesc)
print("Total noise power: {:.2f}dB".format(totalNoisePower_dB))

# Calculating the received power for asc
link2_channelAsc = ChannelElement.channelElement("AWGN")
link2_channelAsc.addGain(gain_dB = link2_asc_tx_antenna_gain_dB)
link2_channelAsc.addAttenuation(attenuation_dB = link2_asc_attenuations)
link2_channelAsc.addAttenuation(attenuation_dB = link2_channelAsc.lossAttenuation(distance = link2_asc_distance, lossModel = "friis", wavelength = utils.FrequencyToWavelength(link2_asc_freq)))
link2_channelAsc.addAttenuation(attenuation_dB = link2_asc_att*480) # Atmosphere is about 480Km
link2_channelAsc.addGain(gain_dB = link2_asc_rx_antenna_gain_dB)
link2_channelAsc.addAttenuation(attenuation_dB = link2_asc_link_margin) # Adding the link margin so we take it into account

signalPowerAsc_dB = link2_channelAsc.calculateRecivedPower(transmittedPower_dB = link2_asc_tx_power_dB)
print("Signal power asc: {:.2f}dB".format(signalPowerAsc_dB))

SNRAsc_dB = signalPowerAsc_dB - noisePowerAsc_dB
print("SNR desc obtained: {:.2f}dB".format(SNRAsc_dB))

link2Asc_Pe = link2_demodulator.get_Pe_from_SNR(SNR_dB = SNRAsc_dB)
print("Pe obtained: {}".format(link2Asc_Pe))

# Calculating the received power for desc
link2_channelDesc = ChannelElement.channelElement("AWGN")
link2_channelDesc.addGain(gain_dB = link2_desc_tx_antenna_gain_dB)
link2_channelDesc.addAttenuation(attenuation_dB = link2_desc_atenuations)
link2_channelDesc.addAttenuation(attenuation_dB = link2_channelDesc.lossAttenuation(distance = link2_desc_distance, lossModel = "friis", wavelength = utils.FrequencyToWavelength(link2_desc_freq)))
link2_channelDesc.addAttenuation(attenuation_dB = link2_desc_att*480) # Atmosphere is about 480Km
link2_channelDesc.addGain(gain_dB = link2_desc_rx_antenna_gain_dB)
link2_channelDesc.addAttenuation(attenuation_dB = link2_desc_link_margin) # Adding the link margin so we take it into account
link2_channelDesc.addGain(gain_dB = amp.calculateEquivalentGain())

signalPowerDesc_dB = link2_channelDesc.calculateRecivedPower(transmittedPower_dB = link2_desc_tx_power_dB)
print("Signal power desc: {:.2f}dB".format(signalPowerDesc_dB))

SNRDesc_dB = signalPowerDesc_dB - noisePowerDesc_dB
print("SNR desc obtained: {:.2f}dB".format(SNRDesc_dB))

link2Desc_Pe = link2_demodulator.get_Pe_from_SNR(SNR_dB = SNRDesc_dB)
print("Pe obtained: {}".format(link2Desc_Pe))

# Section 3



######## Problem 7 ########

# Data
Rb = 5e6 # Bits / s

cable_attenuation = 1.5/1000.0 # dB / m
amp_gain_dB = 15 # dB
amp_figure = 2.5 # dB

BER_objective = 1e-5
modulation = "QPSK"

# Tongitud de cada tramo es 10Km, total 40Km
cable1 = PowerElement.powerElement(attenuation_dB = cable_attenuation, distance = 10000)
amp1 = PowerElement.powerElement(gain_dB = amp_gain_dB, figure = amp_figure, previousElement = cable1)
cable2 = PowerElement.powerElement(attenuation_dB = cable_attenuation, distance = 10000, previousElement = amp1)
amp2 = PowerElement.powerElement(gain_dB = amp_gain_dB, figure = amp_figure, previousElement = cable2)
cable3 = PowerElement.powerElement(attenuation_dB = cable_attenuation, distance = 10000, previousElement = amp2)
amp3 = PowerElement.powerElement(gain_dB = amp_gain_dB, figure = amp_figure, previousElement = cable3)
cable4 = PowerElement.powerElement(attenuation_dB = cable_attenuation, distance = 10000, previousElement = amp3)
amp4 = PowerElement.powerElement(gain_dB = amp_gain_dB, figure = amp_figure, previousElement = cable4)

equivalentTemperature = amp4.calculateEquivalentTemperature()
print("Equivalent temperature: {:.2f}K".format(equivalentTemperature))

demodulator = ModulationElement.modulationElement("QPSK")
noisePower = utils.claculateNoisePower(equivalentTemperature = equivalentTemperature, bandwith = demodulator.get_Bandwith_from_TimeRates(bitRate = Rb)["B"])
noisePower_dB = utils.NaturalToLogarithmic(noisePower)

print("Noise power: {:.2f}dB".format(noisePower_dB))

SNR_dB = demodulator.get_SNR_from_Pe(Pe = demodulator.get_Pe_from_BER(BER_objective))
print("SNR: {:.2f}dB".format(SNR_dB))

print("Transmitted power needed: {:.2f}dB".format(SNR_dB + noisePower_dB))

## Problem 9
freq = 1900e6 # Hz
modulation = "BPSK"
Rb = 250e3 # bits/s

rx_velocity = 100 #Km/h
SNR_average = 20 # dB

# Section 1a (In notebook)

# Section 1b



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
gilbert_transition = [[gilbert_t00, 1 - gilbert_t11], [1 - gilbert_t00, gilbert_t11]]
gilbert_errorProbabilities = [0, gilbert_Pe_bad]
markov = MarkovChain.markovChain(M = 2, T = gilbert_transition, Pe = gilbert_errorProbabilities)
markov.printReleventData()

# Section 2 (#15#2)
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

# Section 3 (#15#3)
k = 26
t = 1
BCH = 45

different_packets_sent = 100000

ARQ_detected_errors = 0
ARQ_missed_errors = 0
ARQ_packets_with_errors = 0
ARQ_packets_sent = 0

FEC_corrected_errors = 0
FEC_missed_errors = 0
FEC_packets_with_errors = 0

FEC_ARQ_corrected_errors = 0
FEC_ARQ_missed_errors = 0
FEC_ARQ_detected_errors = 0
FEC_ARQ_packets_sent = 0
FEC_ARQ_packets_with_errors = 0

for it in range(different_packets_sent):

	# Stop-and-wait ARQ (sw-ARQ)
	not_error = 0
	while not not_error:
		tx_packet = utils.generatePacket(k)
		tx_bits = utils.addCRC(tx_packet, BCH)
		#print("Tx: {}".format(tx_bits))
		errorSequence = markov.simulateModel(n, 0)
		#print("Errors: {}".format(errorSequence))
		rx_bits = utils.binAdd(tx_bits, errorSequence)
		#print("Rx: {}".format(rx_bits))
		not_error = utils.checkCRC(rx_bits, BCH, k)

		# Statistical calculations
		if not (tx_bits == rx_bits).all():
			ARQ_packets_with_errors += 1
			if not_error: ARQ_missed_errors += 1
			else: ARQ_detected_errors += 1

		ARQ_packets_sent += 1


	# FEC
	tx_packet = utils.generatePacket(k)
	tx_bits = utils.addCRC(tx_packet, BCH)
	#print("Tx: {}".format(tx_bits))
	errorSequence = markov.simulateModel(n, 0)
	#print("Errors: {}".format(errorSequence))
	rx_bits = utils.binAdd(tx_bits, errorSequence)
	#print("Rx: {}".format(rx_bits))

	# Statistical calculations
	if not (tx_bits == rx_bits).all():
		# We can correct t errors
		number_of_errors = np.unique(errorSequence, return_counts=True)[1][1]

		FEC_packets_with_errors += 1
		if number_of_errors <= t: FEC_corrected_errors += 1
		else: FEC_missed_errors += 1


	# Híbridas FEC-sw-ARQ
	not_error = 0
	while not not_error:
		tx_packet = utils.generatePacket(k)
		tx_bits = utils.addCRC(tx_packet, BCH)
		#print("Tx: {}".format(tx_bits))
		errorSequence = markov.simulateModel(n, 0)
		#print("Errors: {}".format(errorSequence))
		rx_bits = utils.binAdd(tx_bits, errorSequence)
		#print("Rx: {}".format(rx_bits))
		not_error = utils.checkCRC(rx_bits, BCH, k)

		# Statistical calculations
		if not (tx_bits == rx_bits).all():
			# We can correct t errors
			number_of_errors = np.unique(errorSequence, return_counts=True)[1][1]

			FEC_ARQ_packets_with_errors += 1
			if number_of_errors <= t:
				FEC_ARQ_corrected_errors += 1
				not_error = 1 # We corrected the error
			elif not not_error: FEC_ARQ_detected_errors += 1
			else: FEC_ARQ_missed_errors += 1

		FEC_ARQ_packets_sent += 1


print("ARQ -> Detected errors: {}, missed errors: {}, total errors: {}, total packets: {}".format(ARQ_detected_errors, ARQ_missed_errors, ARQ_packets_with_errors, ARQ_packets_sent))
ARQ_fiability = (1-ARQ_missed_errors/different_packets_sent)*100
P = 1-(ARQ_packets_with_errors/ARQ_packets_sent)
D = 1/Rs # We are sending back 1symbol packets, assimung processing times are none
ARQ_throughput = (k*Rs*P)/(n+D*Rs)
print("ARQ -> Fiability: {:.2f}%, Throughput: {:.2f}bps".format(ARQ_fiability, ARQ_throughput))

print("FEC -> Corrected errors: {}, missed errors: {}, total errors: {}, total packets: {}".format(FEC_corrected_errors, FEC_missed_errors, FEC_packets_with_errors, different_packets_sent))
FEC_fiability = (1-FEC_missed_errors/different_packets_sent)*100
FEC_throughput = (k/n)*Rs
print("FEC -> Fiability: {:.2f}%, Throughput: {:.2f}bps".format(FEC_fiability, FEC_throughput))

print("FEC-ARQ -> Detected errors: {}, missed errors: {}, corrected errors: {}, total errors: {}, total packets: {}".format(FEC_ARQ_detected_errors, FEC_ARQ_missed_errors, FEC_ARQ_corrected_errors, FEC_ARQ_packets_with_errors, FEC_ARQ_packets_sent))
FEC_ARQ_fiability = (1-FEC_ARQ_missed_errors/different_packets_sent)*100
P = 1-((FEC_ARQ_detected_errors+FEC_ARQ_missed_errors)/FEC_ARQ_packets_sent)
D = 1/Rs # We are sending back 1symbol packets, assimung processing times are none
FEC_ARQ_throughput = (k*Rs*P)/(n+D*Rs)
print("FEC-ARQ -> Fiability: {:.2f}%, Throughput: {:.2f}bps".format(FEC_ARQ_fiability, FEC_ARQ_throughput))

# Section 4 (#15#4)
prob_matrix = utils.probErrorInBurst(1, 3, markov.getP(0), markov.getP(1))
print(prob_matrix)