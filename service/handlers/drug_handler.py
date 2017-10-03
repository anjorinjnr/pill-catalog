from handlers.base_handler import BaseHandler
from webapp2 import Route
import logging
from validators.drug_validator import DrugValidator, DrugCategoryValidator
from models import catalog as model
from google.appengine.ext import ndb


class CategoryHandler(BaseHandler):
  def get(self):
    """Return all categories."""
    categories = model.DrugCategory.get_all()
    self.write_model(categories)

  def post(self):
    """Create or update category."""
    data = self.request_data()
    val = DrugCategoryValidator(data=data)
    val.validate()
    if val.errors:
      self.error_response((val.errors))
    else:
      category = model.DrugCategory.save(data)
      self.write_model(category)


class DrugHandler(BaseHandler):
  def get(self, drug_id=None):
    """Return all drugs or drug with specified id."""
    if drug_id:
      drug = model.Drug.get_by_id(int(drug_id))
      if drug:
        categories = model.DrugCategory.get_by_ids(drug.category_ids)
        self.write_model(drug, categories=categories)
      else:
        error = {'message': 'Drug with id({}) not found.'.format(drug_id)}
        self.error_response(error)
    else:
      logging.info('get all')

  def post(self):
    """Create or update drug."""
    data = self.request_data()
    val = DrugValidator(data=data)
    val.validate()
    if val.errors:
      self.error_response(val.errors)
    else:
      drug = model.Drug.save(data)
      self.write_model(drug)


ROUTES = [
  (r'/v1/api/drugs', DrugHandler),
  (r'/v1/api/drugs/(\d+)', DrugHandler),
  (r'/v1/api/categories', CategoryHandler)
]
