import webapp2
import json


from handlers.upload_handler import UploadHandler
from handlers import drug_handler


class BaseHandler(webapp2.RequestHandler):

  def write_response(self, data):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))

  def healthz(self):
    self.write_response({'status': 'up'})

Route = webapp2.Route

routes = [
  (r'/v1/image/upload', UploadHandler),
  Route(r'/v1/healthz',
        handler=BaseHandler,
        handler_method='healthz',
        methods=['GET'])

] + drug_handler.ROUTES

app = webapp2.WSGIApplication(routes, debug=True)