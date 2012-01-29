import cgi
import datetime
import logging
import os
import time

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

# copied from GAE docs
class Pacific_tzinfo(datetime.tzinfo):
  """Implementation of the Pacific timezone."""
  def utcoffset(self, dt):
    return datetime.timedelta(hours=-8) + self.dst(dt)

  def _FirstSunday(self, dt):
    """First Sunday on or after dt."""
    return dt + datetime.timedelta(days=(6-dt.weekday()))

  def dst(self, dt):
    # 2 am on the second Sunday in March
    dst_start = self._FirstSunday(datetime.datetime(dt.year, 3, 8, 2))
    # 1 am on the first Sunday in November
    dst_end = self._FirstSunday(datetime.datetime(dt.year, 11, 1, 1))

    if dst_start <= dt.replace(tzinfo=None) < dst_end:
      return datetime.timedelta(hours=1)
    else:
      return datetime.timedelta(hours=0)
  def tzname(self, dt):
    if self.dst(dt) == datetime.timedelta(hours=0):
      return "PST"
    else:
      return "PDT"


def get_annotated_rsvps():
  # fetch all records, sorted by descending submit time
  rsvp_query = RsvpEntry.all().order('-submit_time')
  all_rsvps = [r for r in rsvp_query]
  # collate by email
  all_rsvps = sorted(all_rsvps, key=attrgetter('email'))

  seen_email = {}
  pacific_time = Pacific_tzinfo()
  for rsvp in all_rsvps:
    # mark all but first entry with given email as "old"
    rsvp.old = seen_email.has_key(rsvp.email)
    seen_email[rsvp.email] = True
    
    # converted stored UTC time to Pacific
    rsvp.submit_time = datetime.datetime.fromtimestamp(time.mktime(rsvp.submit_time.timetuple()), pacific_time)

  return all_rsvps
  
class Dump(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'dump.html')
    all_rsvps = get_annotated_rsvps()

    # count up totals
    total = 0
    total_party = 0
    total_ceremony = 0
    
    for rsvp in all_rsvps:
      # don't count duplicate by email
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
      
    template_values = {
      'all_rsvps': all_rsvps,
      'total': total,
      'total_party': total_party,
      'total_ceremony': total_ceremony
    }
    self.response.out.write(template.render(path, template_values))

class DumpCsv(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-disposition'] = 'attachment; filename=rsvp.csv'
    all_rsvps = get_annotated_rsvps()
    self.response.out.write('Name,Email,Which,Guests,Reply time\n')
    for rsvp in all_rsvps:
      guests = rsvp.guests
      if rsvp.old:
        guests = 0
      csv_row = '%s,%s,%s,%d,%s\n' % (rsvp.name, rsvp.email, rsvp.which, guests, rsvp.submit_time)
      self.response.out.write(csv_row)


application = webapp.WSGIApplication(
                   [('/', MainPage),
                    ('/rsvp', Rsvp),
                    ('/dump', Dump),
                    ('/csv', DumpCsv)],
                   debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
