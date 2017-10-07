import logging
from handlers.base_handler import BaseHandler

from models import catalog as model
from google.appengine.ext import ndb
from google.appengine.api.taskqueue import taskqueue

TASK_URLS = {
  'load_drugs': '/_tasks/load_drugs'
}


class LoadDrugsTaskHandler(BaseHandler):

  @ndb.tasklet
  def _save_entities(self, drugs):
    saved = yield ndb.put_multi(drugs)
    logging.info('saved %s', len(saved))
    raise ndb.Return('saved..')

  def post(self):
    file_name = self.request.get('file_name')
    logging.info('start loading drugs from file:%s', file_name)
    drugs = []
    try:
      with open('data/{}'.format(file_name)) as f:
        lines = f.readlines()
        skipped = lines[15000:]
        for line in skipped:
          items = line.split('\t')
          name = items[0]
          ingredients = items[1]
          manufacturer = items[2]
          registration_no = items[3]
          drugs.append(model.Drug(
            name=name,
            unique_id=registration_no,
            active_ingredients=ingredients,
            manufacturer=manufacturer
          ))
          if len(drugs) == 100:
            logging.info('saving %s drugs from %s', len(drugs), file_name)
            ndb.put_multi(drugs)
            break
            drugs = []
      self.success_response()
    except Exception as ex:
      logging.exception('Error executing task: %s', ex.message)
      self.abort(500)


class QueueTaskHandler(BaseHandler):
  def post(self):
    name = self.request.get('name')
    params = self.request_data()

    if name not in TASK_URLS:
      self.write_plain_response('Invalid task name: {}'.format(name), 400)
      return

    url = TASK_URLS[name]
    task = taskqueue.add(url=url, params=params)
    if task.was_enqueued:
      logging.info('Added task \'%s\' to queue', name)
      self.success_response()
    else:
      self.write_plain_response('Failed to create task', 400)


ROUTES = [
  (r'/_tasks/load_drugs', LoadDrugsTaskHandler),
  (r'/_tasks', QueueTaskHandler)
]
