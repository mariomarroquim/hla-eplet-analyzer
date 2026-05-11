import json
import unittest
from app import app

class SmokeTests(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

  def test_index(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def test_version(self):
    response = self.client.get('/version')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.get_data(as_text=True), '2026-05-09')

  def test_successful_prediction(self):
    params = {
      'eplet_locus': 'abc',
      'eplet_allele_count': 10,
      'eplet_min_mfi': 1000,
      'eplet_max_mfi': 5000,
      'panel_nc': 10,
      'panel_pc': 20000,
    }
    response = self.client.get('/predict', query_string=params)
    response_body = json.loads(response.get_data(as_text=True))

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.mimetype, 'application/json')

    self.assertEqual(response_body['label'], '1')
    self.assertEqual(response_body['score0'], '0.16094096997773463')
    self.assertEqual(response_body['score1'], '0.8390590300222653')

  def test_failed_prediction(self):
    params = {
      'eplet_locus': 'abc',
      'eplet_allele_count': 10,
      'eplet_min_mfi': 1000,
      'eplet_max_mfi': 5000,
    }
    response = self.client.get('/predict', query_string=params)
    response_body = response.get_data(as_text=True)

    self.assertEqual(response.status_code, 500)
    self.assertEqual(response.mimetype, 'text/html')
    self.assertEqual(response_body, 'Check if all params (eplet_locus, eplet_allele_count, eplet_min_mfi, eplet_max_mfi, panel_nc, panel_pc) contain valid values.')

if __name__ == '__main__':
  unittest.main()
