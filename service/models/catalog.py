import logging
import time
from google.appengine.ext import ndb


def not_empty(data, field):
  if field in data and data[field]:
    return True
  else:
    return False


class BaseModel(ndb.Model):
  """Useful attributes and functionality for all Datastore models."""
  created_at = ndb.IntegerProperty()
  created_by = ndb.StringProperty()
  modified_at = ndb.IntegerProperty()
  modified_by = ndb.StringProperty()
  deleted_at = ndb.IntegerProperty()
  deleted_by = ndb.StringProperty()
  deleted = ndb.BooleanProperty()

  def _pre_put_hook(self):
    """Pre-put operations. Store UTC timestamp(s) in milliseconds."""
    now = int(time.time() * 1000)
    self.modified_at = now
    if not self.created_at:
      self.created_at = now
    if self.deleted:
      self.deleted_at = now


class DrugCategory(BaseModel):
  """Broad drug categories e.g vitamins, antibiotics etc."""
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty()


class Drug(BaseModel):
  """Represents a drug without store specific information e.g price."""
  # class constants
  DOSAGE_TABLET = 'Tablet'
  DOSAGE_CREAM = 'Cream'
  DOSAGE_INJECTION = 'Injection'
  DOSAGE_FORMS = [DOSAGE_TABLET, DOSAGE_CREAM, DOSAGE_INJECTION]

  name = ndb.StringProperty(required=True)
  unique_id = ndb.StringProperty(required=True)
  categories = ndb.IntegerProperty(repeated=True)
  dosage_form = ndb.StringProperty(choices=DOSAGE_FORMS)
  pack_size = ndb.IntegerProperty()
  strength = ndb.StringProperty()
  active_ingredients = ndb.StringProperty()
  manufacturer = ndb.StringProperty()

  @classmethod
  def save(cls, data):
    logging.info('saving new drug: %s', data)
    if not not_empty(data, 'id'):
      drug = cls(
        name=data['name'],
        unique_id=data['unique_id']
      )
    else:
      drug = cls.get_by_id(data['id'])

    if not_empty(data, 'categories'):
      drug.categories = data['categories']

    if not_empty(data, 'dosage_form'):
      drug.dosage_form = data['dosage_form']

    if not_empty(data, 'pack_size'):
      try:
        drug.pack_size = int(data['pack_size'])
      except ValueError as e:
        logging.info('invalid pack size: %s', e.message)

    if not_empty(data, 'strength'):
      drug.strength = data['strength']

    if not_empty(data, 'active_ingredients'):
      drug.active_ingredients = data['active_ingredients']

    if not_empty(data, 'manufacturer'):
      drug.manufacturer = data['manufacturer']

    drug.put()
    return drug


class Contact(ndb.Model):
  """An individual."""
  full_name = ndb.StringProperty()
  email = ndb.StringProperty()
  phone_number = ndb.StringProperty()


class Address(ndb.Model):
  """Physical location."""
  street = ndb.StringProperty()
  city = ndb.StringProperty()
  state = ndb.StringProperty()
  country = ndb.StringProperty()


class Pharma(BaseModel):
  """A partner pharmacy selling on the website with > 0 physical stores."""
  name = ndb.StringProperty()
  primary_contact = ndb.StructuredProperty(Contact)
  primary_address = ndb.StructuredProperty(Address)
  website = ndb.StringProperty()


class Store(BaseModel):
  """Represents a physical pharmacy/store where the drugs are fufilled."""
  store_id = ndb.StringProperty()
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  phone = ndb.StringProperty()
  address = ndb.StructuredProperty(Address)
  primary_contact = ndb.StructuredProperty(Contact)


class Product(BaseModel):
  """Individual drug being sold by a store."""
  store_id = ndb.IntegerProperty(required=True)
  pharma_id = ndb.IntegerProperty()
  name = ndb.StringProperty(required=True)
  unique_id = ndb.StringProperty(required=True)
  price = ndb.FloatProperty()
  qty_in_stock = ndb.IntegerProperty()
  manufacture_date = ndb.DateProperty()
  expire_date = ndb.DateProperty()
  batch_no = ndb.StringProperty()
