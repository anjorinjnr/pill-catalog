
import time
import webapp2
import json
import utils

class BaseHandler(webapp2.RequestHandler):
  """Base class for request handlers."""

  def write_model(self, obj, **kwargs):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(utils.encode_model(obj, **kwargs))

  def write_response(self, data):
    # response = webapp2.Response()
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))
    return self.response

  def write_plain_response(self, data):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(data)
    return self.response

  def request_data(self):
    try:
      return json.loads(self.request.body)
    except Exception:  # pylint: disable=broad-except
      return {}


  def current_time(self):
    return int(time.time() * 1000)

  def success_response(self):
    return self.write_response({'status': 'success'})

  def error_response(self, error=''):
    return self.write_response({'status': 'error', 'message': error})