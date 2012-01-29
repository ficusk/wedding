import cgi
import logging
import os

from operator import attrgetter

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

class Rsvp(webapp.RequestHandler):
  def post(self):
    # logging.error(self.request)
    entry = RsvpEntry()
    entry.name = self.request.get('name')
    entry.email = self.request.get('email')
    entry.which = self.request.get('which')
    entry.guests = int(self.request.get('guests'))
    entry.put()

class Dump(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'dump.html')
    rsvp_query = RsvpEntry.all().order('-submit_time')
    all_rsvps = [r for r in rsvp_query]
    all_rsvps = sorted(all_rsvps, key=attrgetter('email'))

    seen_email = {}
    total = 0
    total_party = 0
    total_ceremony = 0
    
    for rsvp in all_rsvps:
      rsvp.old = seen_email.has_key(rsvp.email)
      seen_email[rsvp.email] = True

      if rsvp.old:
        continue
        
      total += rsvp.guests
      if rsvp.which == 'party':
        total_party += rsvp.guests
      elif rsvp.which == 'ceremony':
        total_ceremony += rsvp.guests
      else: # both
        total_party += rsvp.guests
        total_ceremony += rsvp.guests
      
    # self.response.out.write('<html><body>How about:<pre>')
    # for rsvp in all_rsvps:
    #   self.response.out.write("%s (%s): %s - %d / %s<br>" % (rsvp.email, rsvp.name, rsvp.which, rsvp.guests, rsvp.submit_time))
    # self.response.out.write('</pre></body></html>')
    template_values = {
      'all_rsvps': all_rsvps,
      'total': total,
      'total_party': total_party,
      'total_ceremony': total_ceremony
    }
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                   [('/', MainPage),
                    ('/rsvp', Rsvp),
                    ('/dump', Dump)],
                   debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
