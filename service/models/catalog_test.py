import unittest
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from models import catalog as model


class BaseTest(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()
    self.testbed.init_datastore_v3_stub()


class DrugCategoryTest(BaseTest):
  def test_save(self):
    data = {
      'name': 'Vitamins'
    }

    category = model.DrugCategory.save(data)
    self.assertIsNotNone(category)
    self.assertIsNotNone(category.key.id())
    self.assertEqual('Vitamins', category.name)
    self.assertEqual('vitamins', category.name_lower)

  def test_save_avoids_duplicates(self):
    data = {
      'name': 'Vitamins'
    }

    category = model.DrugCategory.save(data)

    category_new = model.DrugCategory.save(data)
    self.assertEqual(category.key, category_new.key)


class DrugTest(BaseTest):
  def test_save_with_category(self):
    data = {
      'name': 'Vitamins'
    }

    category = model.DrugCategory.save(data)
    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'Tablet',
      'categories': [category.key.id()]
    }
    drug = model.Drug.save(data)
    self.assertIsNotNone(drug.key.id())
    self.assertEqual(1, len(drug.category_ids))

  def test_save_ignore_invalid_category(self):

    category_1 = model.DrugCategory(name='Vitamin')
    category_2 = model.DrugCategory(name='Fitness')
    categories = ndb.put_multi([category_1, category_2])

    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'Tablet',
      'categories': [categories[0].id(), 12345]
    }
    drug = model.Drug.save(data)
    self.assertEqual(1, len(drug.category_ids))

  def test_save_update_category(self):

    category_1 = model.DrugCategory(name='Vitamin')
    category_2 = model.DrugCategory(name='Fitness')
    categories = ndb.put_multi([category_1, category_2])

    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'Tablet',
      'categories': [categories[0].id()]
    }
    drug = model.Drug.save(data)
    data['id'] = drug.key.id()
    data['categories'].append(categories[1].id())
    drug = model.Drug.save(data)
    self.assertEqual(2, len(drug.category_ids))

  def test_save(self):
    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'Tablet'
    }
    drug = model.Drug.save(data)
    self.assertIsNotNone(drug)
    self.assertIsNotNone(drug.key.id())
    self.assertEqual('MOPSON', drug.name)
    self.assertEqual('04-2380', drug.unique_id)
    self.assertEqual('Tablet', drug.dosage_form)

  def test_save_updates(self):
    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'Tablet'
    }
    drug = model.Drug.save(data)
    data['id'] = drug.key.id()
    data['dosage_form'] = 'Cream'
    model.Drug.save(data)

    drug = drug.key.get()
    self.assertEqual('Cream', drug.dosage_form)
