#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.

import re
import unittest

FLOAT = r'[-+]?[0-9]*\.?[0-9]+'

def PrefixConverter(to, conversion):
  def PrefixConvertFn(match):
    prefix = match.group(1)
    real = match.group(2)
    spacer = match.group(3)
    usd = float(real) * conversion
    return '%s%s (%s%0.2f)%s' % (prefix, match.group(2), to, usd, spacer)
  return PrefixConvertFn

def PrefixConvert(text, re_from, re_to, to, conversion):
  re_real = re.compile(r'(%(FROM)s)(%(FLOAT)s)([ ,;])(?!\(%(TO)s%(FLOAT)s\))' % dict(
      FROM=re_from, TO=re_to, FLOAT=FLOAT))
  return re_real.sub(PrefixConverter(to, conversion), text)

def PostfixConverter(to, conversion):
  def PostfixConvertFn(match):
    km = match.group(1)
    postfix = match.group(2)
    spacer = match.group(3)
    miles = float(km) * conversion
    return '%s%s (%.2f %s)%s' % (km, postfix, miles, to, spacer)
  return PostfixConvertFn

def PostfixConvert(text, re_from, re_to, to, conversion):
  re_km = re.compile(r'(%(FLOAT)s)(\s?%(FROM)s)([ ,;])(?!\(%(FLOAT)s %(TO)s\))' % dict(
      FROM=re_from, TO=re_to, FLOAT=FLOAT))
  return re_km.sub(PostfixConverter(to, conversion), text)

def ConvertReais(text):
  return PrefixConvert(text, r'R\$\s?', r'\$', '$', 0.518)

def ConvertReais2(text):
  return PrefixConvert(text, r'BRL\$\s?', r'USD\$\s?', r'USD$', 0.518)

def ConvertKm(text):
  return PostfixConvert(text, r'[Kk]m', r'miles', 'miles', 0.6214)

def ConvertKph(text):
  return PostfixConvert(text, r'kph', r'mph', 'mph', 0.6214)

def ConvertKmPerH(text):
  return PostfixConvert(text, r'[Kk]m/h', r'mph', 'mph', 0.6214)


def Converter(text):
  text = ConvertReais(text)
  text = ConvertKm(text)
  text = ConvertKph(text)
  text = ConvertKmPerH(text)
  return text

def TestConvert(expected, test, fn):
  converted = fn(test)
  if converted != expected:
    print 'original  %r' % test
    print 'converted %r' % converted
    print 'expected  %r' % expected
    assert(False)
  if fn != Converter:
    TestConvert(expected, test, Converter)

def Tests():
  TestConvert('R$ 1.00 ($0.52),', 'R$ 1.00,', ConvertReais)
  TestConvert('R$-1.00 ($-0.52),', 'R$-1.00,', ConvertReais)
  TestConvert('R$1 ($0.52),', 'R$1,', ConvertReais)
  TestConvert('It costs R$ 1.00 ($0.52) here', 'It costs R$ 1.00 here', ConvertReais)

  TestConvert('1.23km (0.76 miles),', '1.23km,', ConvertKm)
  TestConvert('-1.23km (-0.76 miles),', '-1.23km,', ConvertKm)
  TestConvert('test 1 km (0.62 miles),', 'test 1 km,', ConvertKm)
  TestConvert('test 1 km (0.62 miles) (', 'test 1 km (', ConvertKm)

  TestConvert('test 1 km (0.62 miles)', 'test 1 km (0.62 miles)', ConvertKm)
  TestConvert('R$ 1.00 ($0.52)', 'R$ 1.00 ($0.52)', ConvertReais)

  TestConvert('100kph (62.14 mph) ', '100kph ', ConvertKph)
  TestConvert('100 km/h (62.14 mph) ', '100 km/h ', ConvertKmPerH)
  # TestConvert(' BRL$1.00 (USD$0.52) ', ' BRL$1.00 ', ConvertReais2)

if __name__ == '__main__':
  Tests()
