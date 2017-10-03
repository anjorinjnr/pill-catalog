import time
import webapp2
import json
import utils

STATUS_ERROR = 400


class BaseHandler(webapp2.RequestHandler):
  """Base class for request handlers."""

  def write_model(self, obj, **kwargs):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(utils.encode_model(obj, **kwargs))


  def write_response(self, data, status=200):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(data))
    self.response.set_status(status)
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

  def success_response(self, data=None):
    if data:
      return self.write_response({'status': 'success'})
    else:
      return self.write_response({'status': 'success', 'data': data})

  def error_response(self, data):
    return self.write_response({'status': 'error', 'data': data},
                               STATUS_ERROR)
