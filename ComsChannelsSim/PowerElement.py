"""
Description:
  This file contains the class for power elements, with this class it can be computed how several connected
  elements behave like only one, to be able to perform calculations faster.
"""

import ComsChannelsSim.utils as utils

class powerElement:
  def __init__(self, **kwargs):
    """
    Parameters:
    * gain in natural units [W]
    * temperature in K
    * figure in dB
    * previous element is class object
    * distance in [m]
    * gainDistance in [dB/m]
    * gain [dB]
    * attenuation [dB]
    * attenuationDistance [dB/m]
    """

    self.distance = kwargs.get("distance", None)

    gain = kwargs.get("gain", None)
    self.gain_dB = kwargs.get("gain_dB", None)
    if self.gain_dB == None and gain != None: self.gain_dB = utils.NaturalToLogarithmic(gain)

    gainDistance = kwargs.get("gainDistance", None)
    gainDistance_dB = kwargs.get("gainDistance_dB", None)
    if gainDistance_dB == None and gainDistance != None: gainDistance_dB = utils.NaturalToLogarithmic(gainDistance)

    attenuation = kwargs.get("attenuation", None)
    self.attenuation_dB = kwargs.get("attenuation_dB", None)
    if self.attenuation_dB == None and attenuation != None: self.attenuation_dB = utils.NaturalToLogarithmic(attenuation)

    attenuationDistance = kwargs.get("attenuationDistance", None)
    attenuationDistance_dB = kwargs.get("attenuationDistance_dB", None)
    if attenuationDistance_dB == None and attenuationDistance != None: attenuationDistance_dB = utils.NaturalToLogarithmic(attenuationDistance)

    # Obtaining gain
    if self.gain_dB == None:
      if gainDistance_dB != None and self.distance != None:
        self.gain_dB = gainDistance_dB * self.distance

      elif self.attenuation_dB != None:
        self.gain_dB = -self.attenuation_dB
      
      elif attenuationDistance_dB != None and self.distance != None:
        self.gain_dB = -(attenuationDistance_dB * self.distance)

      else:
        raise Exception("Gain or attenuation parameters are missing")
    
    # Obtaining attenuation
    if self.attenuation_dB == None:
      self.attenuation_dB = -self.gain_dB

    # Obtaining temperature and figure
    self.temperature = kwargs.get("temperature", None)
    self.figure = kwargs.get("figure", None)
    if self.figure == None: self.figure = self.attenuation_dB
    if self.temperature == None: self.temperature = (self.figure - 1) * 290

    self.previousElement = kwargs.get("previousElement", None)
  
  def calculateEquivalentGain(self):
    """
    Calculates the total gain of all connected power elements, using previous element as reference.

    Returns:
    * EquivalentGain -> The equivalent gain of all the system [dB]
    """

    if self.previousElement == None: return self.gain_dB
    else: return self.gain_dB + self.previousElement.calculateEquivalentGain()
  
  def calculateEquivalentTemperature(self):
    """
    Calculates the equivalent temperature of the complete system, using previous element as reference.

    Returns:
    * EquivalentTemperature -> The equivalent temperature of all the system
    """
    if self.previousElement == None: return self.temperature
    else: 
      return self.previousElement.calculateEquivalentTemperature() + (self.temperature/utils.LogarithmicToNatural(self.previousElement.calculateEquivalentGain()))
  
  def printRelevantData(self, name = None):
    if name != None: print("Information about {}".format(name))
    else: print("Information about power element")
    print("Gain: {:.2f}dBW, {:.2f}W".format(self.gain_dB, utils.LogarithmicToNatural(self.gain_dB)))
    print("Attenuation: {:.2f}dBW, {:.2f}W".format(self.attenuation_dB, utils.LogarithmicToNatural(self.attenuation_dB)))
    print("Temperature: {:.2f}K, Noise figure: {:.2f}dB".format(self.temperature, self.figure))
  
  def printEquivalentValues(self):
    equivalent_gain = self.calculateEquivalentGain()
    equivalent_temperature = self.calculateEquivalentTemperature()
    print("Equivalent gain up to this element: {:.2f}dBW, {:.2f}W".format(equivalent_gain, utils.LogarithmicToNatural(equivalent_gain)))
    print("Figure: {:.2f}dB".format(self.figure))
    print("Temperature: {:.2f}K".format(self.temperature))
    print("Equivalent temperature up to this element: {:.2f}K".format(equivalent_temperature))

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