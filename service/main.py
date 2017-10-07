import webapp2
import json
import logging

from handlers import file_handler
from handlers import drug_handler
from handlers import task_handler

VERSION = '0.5'


class BaseHandler(webapp2.RequestHandler):
  def write_response(self, data):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))


class MetricsHandler(webapp2.RequestHandler):
  def healthz(self):
    self.write_response({'status': 'up', 'version': VERSION})

Route = webapp2.Route

routes = [
           Route(r'/v1/healthz',
                 handler=MetricsHandler,
                 handler_method='healthz',
                 methods=['GET'])

         ] + file_handler.ROUTES + drug_handler.ROUTES

app = webapp2.WSGIApplication(routes, debug=True)

task_queue_app = webapp2.WSGIApplication(task_handler.ROUTES, debug=True)
