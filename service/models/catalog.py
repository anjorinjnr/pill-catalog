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

  _exclude = None

  def _pre_put_hook(self):
    """Pre-put operations. Store UTC timestamp(s) in milliseconds."""
    now = int(time.time() * 1000)
    self.modified_at = now
    if not self.created_at:
      self.created_at = now
    if self.deleted:
      self.deleted_at = now

  def to_dict(self, include=None, exclude=None):
    exclude = self._exclude
    return self._to_dict(include=include, exclude=exclude)


class DrugCategory(BaseModel):
  """Broad drug categories e.g vitamins, antibiotics etc."""
  name = ndb.StringProperty(required=True)
  name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
  description = ndb.StringProperty()

  @classmethod
  def get_by_ids(cls, ids):
    categories = []
    if ids:
      keys = [ndb.Key(DrugCategory, k) for k in ids]
      categories = cls.query().filter(DrugCategory.key.IN(keys)).fetch(
        projection=['name', 'description'])

    return categories

  @classmethod
  def get_all(cls):
    return cls.query().fetch(projection=['name', 'description'])

  @classmethod
  def save(cls, data):
    name = data['name']
    category = cls.query(DrugCategory.name_lower == name.lower().strip()).get()
    if not category:
      category = DrugCategory(name=name.strip())
      if not_empty(data, 'description'):
        category.description = data['description']
      category.put()
    return category


class Drug(BaseModel):
  """Represents a drug without store specific information e.g price."""
  # class constants
  DOSAGE_TABLET = 'Tablet'
  DOSAGE_CREAM = 'Cream'
  DOSAGE_INJECTION = 'Injection'
  DOSAGE_FORMS = [DOSAGE_TABLET, DOSAGE_CREAM, DOSAGE_INJECTION]

  PAGE_SIZE = 50

  name = ndb.StringProperty(required=True)
  unique_id = ndb.StringProperty(required=True)
  category_ids = ndb.IntegerProperty(repeated=True)
  dosage_form = ndb.StringProperty(choices=DOSAGE_FORMS)
  pack_size = ndb.IntegerProperty()
  strength = ndb.StringProperty()
  active_ingredients = ndb.StringProperty()
  manufacturer = ndb.StringProperty()
  details = ndb.TextProperty(default='')

  images = ndb.StringProperty(repeated=True)

  _exclude = ['category_ids']

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
      category_ids = []
      for category in data['categories']:
        if isinstance(category, dict) and 'id' in category:
          category_ids.append(long(category['id']))
        elif isinstance(category, long) or isinstance(category, int):
          category_ids.append(long(category))

      category_keys = [ndb.Key(DrugCategory, i) for i in category_ids]
      categories = ndb.get_multi(category_keys)
      categories = [c for c in categories if c is not None]
      drug.category_ids = [c.key.id() for c in categories]

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

    if not_empty(data, 'details'):
      drug.details = data['details']

    drug.put()
    return drug

  @classmethod
  def get_all(cls, offset=0, limit=PAGE_SIZE):

    offset = offset - 1 if offset > 0 else 0

    @ndb.tasklet
    def callback(drug):
      categories = []
      if drug.category_ids:
        category_keys = [ndb.Key(DrugCategory, c) for c in drug.category_ids]
        categories = yield DrugCategory.query().filter(
          DrugCategory.key.IN(category_keys)).fetch_async(
          projection=['name', 'description'])

      raise ndb.Return((drug, categories))


    total_future = cls.query().count_async(keys_only=True)
    query = cls.query().order(cls.name)
    data = query.fetch(limit, offset=offset)

    data_with_related = []
    for d in data:
      data_with_related.append(callback(d).get_result())
    total = total_future.get_result()

    return {
      'data': data_with_related,
      'page_total': len(data_with_related),
      'from': offset + 1 if offset < total else None,
      'to': offset + len(data_with_related) if data_with_related else None,
      'next': offset + limit + 1 if offset + limit + 1 <= total else None,
      'total': total,
      'page_size': limit
    }


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
  """Represents a physical pharmacy/store where the drugs.js are fufilled."""
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
