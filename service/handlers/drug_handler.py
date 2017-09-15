from handlers.base_handler import BaseHandler
from webapp2 import Route
import logging
from validators.drug_validator import DrugValidator
from models import catalog as model


class DrugHandler(BaseHandler):
  def post(self):
    data = self.request_data()
    val = DrugValidator(data=data)
    val.validate()
    if val.errors:
      self.error_response(val.errors)
    else:
      drug = model.Drug.save(data)
      self.write_model(drug)


ROUTES = [
  (r'/v1/api/drug', DrugHandler)
]
