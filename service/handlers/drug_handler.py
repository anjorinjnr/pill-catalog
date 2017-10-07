from handlers.base_handler import BaseHandler
import logging
from validators.drug_validator import DrugValidator, DrugCategoryValidator
from models import catalog as model
import utils


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
     offset = self.request.get('offset', default_value=0)
     try:
       offset = int(offset)
     except ValueError:
       offset = 0
       logging.error('Invalid offset')

     results = model.Drug.get_all(offset=int(offset))
     data = []
     for drugs in results['data']:
       data.append(utils.model_to_dict(drugs[0], categories=drugs[1]))
     results['data'] = data
     self.write_model(results)

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
