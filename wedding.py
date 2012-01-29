import cgi
import logging
import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))

class RsvpEntry(db.Model):
  name = db.StringProperty()
  email = db.StringProperty()
  which = db.StringProperty()
  guests = db.IntegerProperty()
  submit_time = db.DateTimeProperty(auto_now=True)
  pass

class Rsvp(webapp.RequestHandler):
  def post(self):
    # logging.error(self.request)
    entry = RsvpEntry()
    entry.name = self.request.get('name')
    entry.email = self.request.get('email')
    entry.which = self.request.get('which')
    entry.guests = int(self.request.get('guests'))
    entry.put()

application = webapp.WSGIApplication(
                   [('/', MainPage),
                    ('/rsvp', Rsvp)],
                   debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
