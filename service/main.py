import webapp2
import json
import logging

from handlers import file_handler
from handlers import drug_handler


class BaseHandler(webapp2.RequestHandler):

  def write_response(self, data):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))

  def healthz(self):
    self.write_response({'status': 'up'})

Route = webapp2.Route

routes = [
  Route(r'/v1/healthz',
        handler=BaseHandler,
        handler_method='healthz',
        methods=['GET'])

] + file_handler.ROUTES + drug_handler.ROUTES

app = webapp2.WSGIApplication(routes, debug=True)