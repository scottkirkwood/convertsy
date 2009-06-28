# Show something instead of 404 error

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    text = """Scott Kirkwood's Google Wave Robot<br>
        See the <a href="http://code.google.com/p/convertsy">home page</a> 
        for more information about this robot."""

    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(text)

application = webapp.WSGIApplication([('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
