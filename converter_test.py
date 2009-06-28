#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Google Inc. All Rights Reserved.
import unittest
import converter

class ConverterTest(unittest.TestCase):
  def TestConvert(self, expected, test, fn):
    converted = fn(test)
    if converted != expected:
      print 'original  %r' % test
      print 'converted %r' % converted
      print 'expected  %r' % expected
      self.assertEquals(expected, converted)
    self.TestGeneralConverter(expected, test)

  def TestGeneralConverter(self, expected, test):
    converted = converter.Converter(test)
    if converted != expected:
      print '**** General converter issue ****'
      print 'original  %r' % test
      print 'converted %r' % converted
      print 'expected  %r' % expected
      self.assertEquals(expected, converted)

  def testReais(self):
    self.TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($?)', converter.ConvertReais)
    self.TestConvert('R$-1.00 ($-0.52)', 'R$-1.00 ($??)', converter.ConvertReais)
    self.TestConvert('R$1($0.5)', 'R$1($?)', converter.ConvertReais)
    self.TestConvert('It costs R$ 1.00 ($ 0.52) here', 'It costs R$ 1.00 ($ ?) here', converter.ConvertReais)
    self.TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($0.52)', converter.ConvertReais)
    self.TestConvert(' BRL$1.00 (USD$ 0.52)', ' BRL$1.00 (USD$ ?)', converter.ConvertReais)

  def testKm(self): 
    self.TestConvert('1.23km (0.76 miles)', '1.23km (? miles)', converter.ConvertKm)
    self.TestConvert('1 mile (1.6 km)', '1 mile (? km)', converter.ConvertKm)
    self.TestConvert('-1.23km (-0.76 miles)', '-1.23km (? miles)', converter.ConvertKm)
    self.TestConvert('test 1 km (0.6 miles)', 'test 1 km (? miles)', converter.ConvertKm)
    self.TestConvert('test 1 km (bob miles)', 'test 1 km (bob miles)', converter.ConvertKm)

    self.TestConvert('test 1 km (0.6 miles)', 'test 1 km (? miles)', converter.ConvertKm)

  def testKph(self):
    self.TestConvert('100kph (62.1 mph)', '100kph (? mph)', converter.ConvertKph)
    self.TestConvert('100mph (161 kph)', '100mph (? kph)', converter.ConvertKph)
    self.TestConvert('100 km/h (62.1 mph)', '100 km/h (? mph)', converter.ConvertKph)

  def testCelsius(self):
    self.TestConvert('100F (37.8C)', '100F (?C)', converter.ConvertCelcius)
    self.TestConvert('100°C (212°F)', '100°C (?°F)', converter.ConvertCelcius)

  def testCentimeters(self):
    self.TestConvert('2.54cm (1.00")', '2.54cm (?")', converter.ConvertCm)
    self.TestConvert('1 inch (2.54 centimeters)', '1 inch (? centimeters)', converter.ConvertCm)

  def testCentimeters(self):
    self.TestConvert('100kg (220lbs)', '100kg (?lbs)', converter.ConvertKg)
    self.TestConvert('220 pounds (100 Kg)', '220 pounds (? Kg)', converter.ConvertKg)

  def testNumFigs(self):
    self.assertEquals(4, converter.NumSigFigs('0.123'))
    self.assertEquals(0, converter.NumSigFigs(''))
    self.assertEquals(2, converter.NumSigFigs('12'))
    self.assertEquals(3, converter.NumSigFigs('.123'))

  def testSameSigFigs(self):
     self.assertEquals('1', converter.SameSigFigs(1.02, 1))
     self.assertEquals('1.2', converter.SameSigFigs(1.23, 2))
     self.assertEquals('1.23', converter.SameSigFigs(1.23, 3))
     self.assertEquals('1.230', converter.SameSigFigs(1.23, 4))
     self.assertEquals('123', converter.SameSigFigs(123.45, 1))
     self.assertEquals('123.4', converter.SameSigFigs(123.45, 4))
    
if __name__ == '__main__':
  unittest.main()

