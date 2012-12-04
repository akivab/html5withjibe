"""
End points for health applications.
"""

# Generic modules.
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail

import os, re
from django.utils import simplejson

## JSON endpoints.

## HTML pages.
class GamePage(webapp.RequestHandler):
  def get(self):
    pages = {'/index': 'index.html',
      '/to25': 'popto25.html',
      '/addmodal': 'addmodal.html',
      '/bubblepop': 'bubblepop.html',
      '/gameportal': 'game_portal.html' }
    path = self.request.path
    for page in pages:
      if re.match(page, path):
        self.write_out(pages[page])
        return
    self.write_out(pages['/index'])

  def post(self):
    name = self.request.get("name")  
    email = self.request.get("email")
    message = self.request.get("message")

    mail.send_mail(sender="BeeYunks! <akiva@wesosmart.com>",
                  to="akiva.bamberger@gmail.com, david.lluncor@gmail.com",
                  subject="Message from %s" % name,
                  body="""
From %s (email: %s):

%s
""" % (name, email, message))
    self.redirect("/index#email_received")
  
  def write_out(self, url):
    values = {}
    path = os.path.join(os.path.dirname(__file__), 'templates', url)
    self.response.out.write(template.render(path, values))

def main():
  run_wsgi_app(webapp.WSGIApplication([('/.*', GamePage)], debug=False))

if __name__ == '__main__':
  main()
