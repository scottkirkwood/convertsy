#!/usr/bin/python2.4
#

"""Utilities

Useful common routines should go here:
- @ForceLogin() decorator to ensure the user is logged in.

"""

__author__ = 'scottakirkwood@gmail.com (Scott Kirkwood)'

from google.appengine.api import users

def ForceLogin():
  """Creates a decorator that guarantees the user is logged in.

  If the user isn't logged in we redirect to the login page.

  Example usage
  >>> import util
  >>> class MyClass(webapp.RequestHandler):
  >>>   @util.ForceLogin()
  >>>   def get(self):
  >>>     pass # user never reaches here if not logged in.

  Returns:
    decorator that forces login if not logged in to gae.
  """

  def _CheckLogin(func):
    def _CheckLoginFunc(self, *args, **kwargs):
      user = users.get_current_user()
      if not user:
        self.redirect(users.CreateLoginURL(self.request.uri))
      return func(self, *args, **kwargs)
    return _CheckLoginFunc
  return _CheckLogin


def ForceAdminLogin():
  """Creates a decorator that guarantees the user is logged in as admin.

  If the user isn't logged in as admin we show a 404 error.

  Example usage
  >>> import util
  >>> class MyClass(webapp.RequestHandler):
  >>>   @util.ForceAdminLogin()
  >>>   def get(self):
  >>>     pass # user never reaches here if not amdin.

  Returns:
    decorator that forces login if not logged in to gae.
  """

  def _CheckLogin(func):
    def _CheckLoginFunc(self, *args, **kwargs):
      if not users.is_current_user_admin():
        self.error(404)
      return func(self, *args, **kwargs)
    return _CheckLoginFunc
  return _CheckLogin

def SafeFloat(val):
  if val:
    return float(val)
  return 0.0

def SafeInt(val):
  if val:
    return int(val)
  return 0

def NullForZero(val):
  if val:
    return val
  return None

def BlankForZero(val):
  if val:
    return val
  return ''
