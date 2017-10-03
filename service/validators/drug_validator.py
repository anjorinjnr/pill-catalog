from wtforms import Form, BooleanField, StringField, IntegerField
from wtforms.validators import DataRequired



class DrugValidator(Form):
  "Validator for the Drug model."""
  name = StringField('name', [DataRequired(message='Name is required.')])
  unique_id = StringField('unique_id', [DataRequired(message='Unique Id is required.')])

class DrugCategoryValidator(Form):
  "Validator for the DrugCategory model."""
  name = StringField('name', [DataRequired(message='Name is required.')])
