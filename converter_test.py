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
      self.assertTrue(False)
    self.TestGeneralConverter(expected, test)

  def TestGeneralConverter(self, expected, test):
    converted = converter.Converter(test)
    if converted != expected:
      print '**** General converter issue ****'
      print 'original  %r' % test
      print 'converted %r' % converted
      print 'expected  %r' % expected
      self.assertTrue(False)

  def testReais(self):
    self.TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($?)', converter.ConvertReais)
    self.TestConvert('R$-1.00 ($-0.52)', 'R$-1.00 ($??)', converter.ConvertReais)
    self.TestConvert('R$1($0.52)', 'R$1($?)', converter.ConvertReais)
    self.TestConvert('It costs R$ 1.00 ($ 0.52) here', 'It costs R$ 1.00 ($ ?) here', converter.ConvertReais)
    self.TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($0.52)', converter.ConvertReais)

  def testKm(self): 
    self.TestConvert('1.23km (0.76 miles)', '1.23km (? miles)', converter.ConvertKm)
    self.TestConvert('1 mile (1.61 km)', '1 mile (? km)', converter.ConvertKm)
    self.TestConvert('-1.23km (-0.76 miles)', '-1.23km (? miles)', converter.ConvertKm)
    self.TestConvert('test 1 km (0.62 miles)', 'test 1 km (? miles)', converter.ConvertKm)
    self.TestConvert('test 1 km (bob miles)', 'test 1 km (bob miles)', converter.ConvertKm)

    self.TestConvert('test 1 km (0.62 miles)', 'test 1 km (? miles)', converter.ConvertKm)

  def testKph(self):
    self.TestConvert('100kph (62.14 mph)', '100kph (? mph)', converter.ConvertKph)
    self.TestConvert('100mph (160.93 kph)', '100mph (? kph)', converter.ConvertKph)
    self.TestConvert('100 km/h (62.14 mph)', '100 km/h (? mph)', converter.ConvertKph)
    self.TestConvert(' BRL$1.00 (USD$ 0.52)', ' BRL$1.00 (USD$ ?)', converter.ConvertReais)

  def testCelsius(self):
    self.TestConvert('100F (37.78C)', '100F (?C)', converter.ConvertCelcius)
    self.TestConvert('100°C (212.00°F)', '100°C (?°F)', converter.ConvertCelcius)

  def testCentimeters(self):
    self.TestConvert('2.54cm (1.00")', '2.54cm (?")', converter.ConvertCm)
    self.TestConvert('1 inch (2.54 centimeters)', '1 inch (? centimeters)', converter.ConvertCm)

if __name__ == '__main__':
  unittest.main()

