import cgi
import cloudstorage
import os
from google.appengine.api import app_identity
import logging
from models import catalog as model
from handlers.base_handler import BaseHandler
import hashlib
import webapp2
import re


BUCKET_NAME = 'rx-images'


class ImageHandler(BaseHandler):
  def get(self, image_path):
    self.response.headers['Content-Type'] = 'image/jpg'
    filename = '/{}'.format(image_path)

    with cloudstorage.open(filename) as cloudstorage_file:
      self.response.write(cloudstorage_file.read())

    logging.info(image_path)

  def list_images(self):
    page_size = 1
    stats = cloudstorage.listbucket(BUCKET_NAME, max_keys=page_size)
    while True:
      count = 0
      for stat in stats:
        count += 1
        self.response.write(repr(stat))
        self.response.write('\n')

      if count != page_size or count == 0:
        break
      stats = cloudstorage.listbucket(BUCKET_NAME, max_keys=page_size,
                                      marker=stat.filename)


class UploadHandler(BaseHandler):
  def post(self):
    bucket_name = os.environ.get(
      'BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

    drug_id = self.request.get('drug_id')
    logging.info('upload for drug: %s', drug_id)
    drug = model.Drug.get_by_id(int(drug_id))

    image = self.request.POST.get('file', None)
    if isinstance(image, cgi.FieldStorage):
      file_name = self.create_file(image)
      drug.images.append(file_name)
      drug.put()
      self.write_response({'file_name': file_name});

  def create_file(self, file):
    """Create a file."""

    m = hashlib.md5()
    m.update(file.filename)
    m.update(str(self.current_time()))

    ext = ''
    match = re.search(r'\.(.{3})$', file.filename)
    if match:
      ext = match.group(0)

    filename = '/{}/{}{}'.format(BUCKET_NAME, m.hexdigest(), ext)
    logging.info('saving file(%s) at %s', file.type, filename)

    options = {}
    # The retry_params specified in the open call will override the default
    # retry params for this particular file handle.
    write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)
    with cloudstorage.open(filename, 'w', content_type=file.type,
                           options=options, retry_params=write_retry_params
                           ) as cloudstorage_file:
      cloudstorage_file.write(file.file.read())

    return filename


ROUTES = [
  webapp2.Route(r'/v1/images/list',
                handler='handlers.file_handler.ImageHandler:list_images'),
  (r'/v1/images/(.*)', ImageHandler),
  (r'/v1/image/upload', UploadHandler),
]
