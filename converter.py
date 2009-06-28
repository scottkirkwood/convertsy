#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Copyright 2009 Google Inc. All Rights Reserved.

import re

FLOAT = r'[-+]?[0-9]*\.?[0-9]+'
QUESTS = r'\?+'
OPTSPACES = r'\s*'

def PrefixConverter(conversion_fn):
  def PrefixConvertFn(match):
    from_type, space1, from_num, space2, to_type, space3 = match.groups()
    to_num = '%0.2f' % conversion_fn(from_type, to_type, float(from_num))
    return '%(FROM_TYPE)s%(SPACE1)s%(FROM_NUM)s%(SPACE2)s(%(TO_TYPE)s%(SPACE3)s%(TO_NUM)s)' % dict(
        FROM_TYPE=from_type, SPACE1=space1, SPACE2=space2, SPACE3=space3, FROM_NUM=from_num, 
        TO_TYPE=to_type, TO_NUM=to_num)
  return PrefixConvertFn

def PrefixConvert(text, re_from, re_to, conversion_fn):
  re_str = r'(%(FROM)s)(%(SPACES)s)(%(FLOAT)s)(%(SPACES)s)\((%(TO)s)(%(SPACES)s)%(QUESTS)s\)' % dict(
      FROM=re_from, TO=re_to, SPACES=OPTSPACES, FLOAT=FLOAT, QUESTS=QUESTS)
  re_find = re.compile(re_str)
  return re_find.sub(PrefixConverter(conversion_fn), text)

def PostfixConverter(conversion_fn):
  def PostfixConvertFn(match):
    from_num, space1, from_type, space2, space3, to_type = match.groups()
    to_num = '%0.2f' % conversion_fn(from_type, to_type, float(from_num))
    return '%(FROM_NUM)s%(SPACE1)s%(FROM_TYPE)s%(SPACE2)s(%(TO_NUM)s%(SPACE3)s%(TO_TYPE)s)' % dict(
        FROM_NUM=from_num, FROM_TYPE=from_type, TO_NUM=to_num, TO_TYPE=to_type, 
        SPACE1=space1, SPACE2=space2, SPACE3=space3)
  return PostfixConvertFn

def PostfixConvert(text, re_from, re_to, conversion_fn):
  re_str = r'(%(FLOAT)s)(%(SPACES)s)(%(FROM)s)(%(SPACES)s)\(%(QUESTS)s(%(SPACES)s)(%(TO)s)\)' % dict(
      FROM=re_from, TO=re_to, SPACES=OPTSPACES, FLOAT=FLOAT, QUESTS=QUESTS)
  re_find = re.compile(re_str)
  return re_find.sub(PostfixConverter(conversion_fn), text)

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

