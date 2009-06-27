#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Copyright 2009 Google Inc. All Rights Reserved.

import re
import unittest

FLOAT = r'[-+]?[0-9]*\.?[0-9]+'
QUESTS = r'\?+'
OPTSPACES = r'\s*'

def PrefixConverter(conversion_fn):
  def PrefixConvertFn(match):
    from_type, space1, from_num, space2, to_type, space3 = match.groups()
    to_num = '%0.2f' % conversion_fn(from_type, to_type, float(from_num))
    return '%(PREFIX)s%(SPACE1)s%(REAL)s%(SPACE2)s(%(TO)s%(SPACE3)s%(USD)s)' % dict(
        PREFIX=from_type, SPACE1=space1, SPACE2=space2, SPACE3=space3, REAL=from_num, 
        TO=to_type, USD=to_num)
  return PrefixConvertFn

def PrefixConvert(text, re_from, re_to, conversion_fn):
  re_str = r'(%(FROM)s)(%(SPACES)s)(%(FLOAT)s)(%(SPACES)s)\((%(TO)s)(%(SPACES)s)%(QUESTS)s\)' % dict(
      FROM=re_from, TO=re_to, SPACES=OPTSPACES, FLOAT=FLOAT, QUESTS=QUESTS)
  re_real = re.compile(re_str)
  return re_real.sub(PrefixConverter(conversion_fn), text)

def PostfixConverter(conversion_fn):
  def PostfixConvertFn(match):
    from_num, space1, from_type, space2, space3, to_type = match.groups()
    to_num = '%0.2f' % conversion_fn(from_type, to_type, float(from_num))
    return '%(KM)s%(SPACE1)s%(POST)s%(SPACE2)s(%(MILES)s%(SPACE3)s%(TO)s)' % dict(
        KM=from_num, POST=from_type, MILES=to_num, TO=to_type, SPACE1=space1, SPACE2=space2, SPACE3=space3)
  return PostfixConvertFn

def PostfixConvert(text, re_from, re_to, conversion_fn):
  re_str = r'(%(FLOAT)s)(%(SPACES)s)(%(FROM)s)(%(SPACES)s)\(%(QUESTS)s(%(SPACES)s)(%(TO)s)\)' % dict(
      FROM=re_from, TO=re_to, SPACES=OPTSPACES, FLOAT=FLOAT, QUESTS=QUESTS)
  re_km = re.compile(re_str)
  return re_km.sub(PostfixConverter(conversion_fn), text)

def InvertFn(fn):
  def InvertedFn(from_type, to_type, num):
    return 1.0 / fn(to_type, from_type, 1.0 / num)
  return InvertedFn

def PrefixConverters(text, re_from, re_to, conversion_fn):
  text = PrefixConvert(text, re_from, re_to, conversion_fn)
  return PrefixConvert(text, re_to, re_from, InvertFn(conversion_fn))

def PostfixConverters(text, re_from, re_to, conversion_fn):
  text = PostfixConvert(text, re_from, re_to, conversion_fn)
  return PostfixConvert(text, re_to, re_from, InvertFn(conversion_fn))

def ReaisConvert(from_type, to_type, from_num):
  return 0.518 * from_num

def ConvertReais(text):
  return PrefixConverters(text, r'R\s?\$|BRL\s?\$', r'\$|USD\s?\$', ReaisConvert)

def KmConvert(from_type, to_type, from_num):
  return 0.6214 * from_num

def ConvertKm(text):
  return PostfixConverters(text, r'[Kk]m', r'miles?', KmConvert)

def CmConvert(from_type, to_type, from_num):
  return 1/2.54 * from_num

def ConvertCm(text):
  return PostfixConverters(text, r'cm|centimeters?', r'"|inch(?:es)?', CmConvert)
def ConvertKph(text):
  return PostfixConverters(text, r'[Kk]m/h|kph', r'[Mm]ph|miles? per hour', KmConvert)

def CelsiusToF(from_type, to_type, from_num):
  return (9. / 5) * from_num + 32.0

def FToCelsius(from_type, to_type, from_num):
  return (5. / 9) * (from_num - 32.0)

def ConvertCelcius(text):
  c_regex = r'[Cc]|[C]elsius|°C'
  f_regex = r'[Ff]|[Ff]ahrenheit|°F'
  text = PostfixConvert(text, c_regex, f_regex, CelsiusToF)
  return PostfixConvert(text, f_regex, c_regex, FToCelsius) 

def Converter(text):
  text = ConvertReais(text)
  text = ConvertKm(text)
  text = ConvertKph(text)
  text = ConvertCelcius(text)
  text = ConvertCm(text)
  return text

def TestConvert(expected, test, fn):
  converted = fn(test)
  if converted != expected:
    print 'original  %r' % test
    print 'converted %r' % converted
    print 'expected  %r' % expected
    assert(False)
  TestGeneralConverter(expected, test)

def TestGeneralConverter(expected, test):
  converted = Converter(test)
  if converted != expected:
    print '**** General converter issue ****'
    print 'original  %r' % test
    print 'converted %r' % converted
    print 'expected  %r' % expected
    assert(False)

def Tests():
  TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($?)', ConvertReais)
  TestConvert('R$-1.00 ($-0.52)', 'R$-1.00 ($??)', ConvertReais)
  TestConvert('R$1($0.52)', 'R$1($?)', ConvertReais)
  TestConvert('It costs R$ 1.00 ($ 0.52) here', 'It costs R$ 1.00 ($ ?) here', ConvertReais)

  TestConvert('1.23km (0.76 miles)', '1.23km (? miles)', ConvertKm)
  TestConvert('1 mile (1.61 km)', '1 mile (? km)', ConvertKm)
  TestConvert('-1.23km (-0.76 miles)', '-1.23km (? miles)', ConvertKm)
  TestConvert('test 1 km (0.62 miles)', 'test 1 km (? miles)', ConvertKm)
  TestConvert('test 1 km (bob miles)', 'test 1 km (bob miles)', ConvertKm)

  TestConvert('test 1 km (0.62 miles)', 'test 1 km (? miles)', ConvertKm)
  TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($0.52)', ConvertReais)

  TestConvert('100kph (62.14 mph)', '100kph (? mph)', ConvertKph)
  TestConvert('100mph (160.93 kph)', '100mph (? kph)', ConvertKph)
  TestConvert('100 km/h (62.14 mph)', '100 km/h (? mph)', ConvertKph)
  TestConvert(' BRL$1.00 (USD$ 0.52)', ' BRL$1.00 (USD$ ?)', ConvertReais)

  TestConvert('100F (37.78C)', '100F (?C)', ConvertCelcius)
  TestConvert('100°C (212.00°F)', '100°C (?°F)', ConvertCelcius)

  TestConvert('2.54cm (1.00")', '2.54cm (?")', ConvertCm)
  TestConvert('1 inch (2.54 centimeters)', '1 inch (? centimeters)', ConvertCm)

if __name__ == '__main__':
  Tests()
