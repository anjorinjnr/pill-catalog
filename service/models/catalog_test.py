
import unittest
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from models import catalog as model

class DrugModelTest(unittest.TestCase):

  def setUp(self):
    self.testbed= testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()
    self.testbed.init_datastore_v3_stub()

  def test_save(self):
    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'tablet'
    }
    drug = model.Drug.save(data)
    self.assertIsNotNone(drug)
    self.assertIsNotNone(drug.key.id())
    self.assertEqual('MOPSON', drug.name)
    self.assertEqual('04-2380', drug.unique_id)
    self.assertEqual('tablet', drug.dosage_form)

  def test_save_updates(self):
    data = {
      'name': 'MOPSON',
      'unique_id': '04-2380',
      'dosage_form': 'tablet'
    }
    drug = model.Drug.save(data)
    data['id'] = drug.key.id()
    data['dosage_form'] = 'cream'
    model.Drug.save(data)

    drug = drug.key.get()
    self.assertEqual('cream', drug.dosage_form)
