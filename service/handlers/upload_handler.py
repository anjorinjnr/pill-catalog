import cgi
import cloudstorage
import os
from google.appengine.api import app_identity
import logging
from google.appengine.ext import ndb

from handlers.base_handler import BaseHandler


BUCKET_NAME = 'rx-images'
class UploadHandler(BaseHandler):

  def post(self):
    bucket_name = os.environ.get(
      'BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

    print bucket_name
    image = self.request.POST.get('file', None)
    drug_id = self.request.POST.get('drug_id')
    logging.info('drug id: %s', drug_id)
    if isinstance(image, cgi.FieldStorage):
      self.create_file(image)

  def create_file(self, file):
    """Create a file."""

    logging.info('Creating file {}\n'.format(file.filename))

    new_id = ndb.Model.allocate_ids(size=1)[0]

    filename = '/%s/%s' % (BUCKET_NAME, new_id)
    print filename

    # The retry_params specified in the open call will override the default
    # retry params for this particular file handle.
    write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)
    with cloudstorage.open(
      filename, 'w', content_type=file.type, options={
        'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'},
      retry_params=write_retry_params) as cloudstorage_file:
      cloudstorage_file.write(file.file.read())
