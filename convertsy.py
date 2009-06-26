#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
from waveapi import events
from waveapi import model
from waveapi import robot
import converter

def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for p in added:
    Notify(context)

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("I'm alive!")

def Notify(context):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hi everybody!")

def OnBlipChanged(properties, context):
  blip = context.GetBlipById(properties['blipId'])
  text = blip.GetDocument().GetText()
  blip.GetDocument().SetText(converter.Converter(text))

def trace(msg, context):
  """Output trace info to blip"""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("convertsy trace: %s" % msg)

if __name__ == '__main__':
  myRobot = robot.Robot('convertsy', 
      image_url='http://convertsy.appspot.com/icon.png',
      version='4',
      profile_url='http://convertsy.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipChanged)
  myRobot.Run(debug=True)
