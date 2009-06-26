#!/usr/bin/python
#

"""Schema used for the weight log app."""

__author__ = 'scottakirkwood@gmail.com (Scott Kirkwood)'

from google.appengine.ext import db


class WeightEntry(db.Model):
  """The data schema for Weight Entry."""
  user = db.UserProperty(required=True)
  date = db.DateProperty(required=True)
  weight_kg = db.FloatProperty()
  workout_min = db.FloatProperty()
  running_km = db.FloatProperty()
  sld_calories = db.IntegerProperty()
  is_iso = db.BooleanProperty()
  comment = db.StringProperty()
  timestamp = db.DateTimeProperty(auto_now_add=True)
