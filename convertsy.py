#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
from waveapi import events
from waveapi import model
from waveapi import robot
import converter

WELCOME_TEXT = """Hi, I'm convertsy.
Type '123 km (? miles)' to convert to miles (and vice-versa). 
Also 'R$123.00 ($ ?)' to convert Reais to US dollars.
I can convert:
  kg Kg <-> lbs pounds
  liters L l <-> gallons gal gal.
  cm <-> inches "
  celsius C <-> fahrenheit F
"""

def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for p in added:
    Notify(context)

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText(WELCOME_TEXT)

def Notify(context):
  root_wavelet = context.GetRootWavelet()
  #root_wavelet.CreateBlip().GetDocument().SetText("Hi everybody!")

def OnBlipChanged(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  text = blip.GetDocument().GetText()
  newtext = converter.Converter(text) 
  if newtext != text:
    blip.GetDocument().SetText(newtext)

def DocumentChanged(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  text = blip.GetDocument().GetText()
  newtext = converter.Converter(text) 
  if newtext != text:
    blip.GetDocument().SetText(newtext)

def trace(msg, context):
  """Output trace info to blip"""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("convertsy trace: %s" % msg)

if __name__ == '__main__':
  myRobot = robot.Robot('convertsy', 
      image_url='http://convertsy.appspot.com/icon.png',
      version='2',
      profile_url='http://convertsy.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipChanged)
  myRobot.RegisterHandler(events.DOCUMENT_CHANGED, DocumentChanged)
  myRobot.Run(debug=True)
