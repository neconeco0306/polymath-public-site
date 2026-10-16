import json, unittest
from pathlib import Path
ROOT=Path(__file__).parent

class PublicResearchEvidenceTests(unittest.TestCase):
 def test_claims_crosscheck(self):
  d=json.loads((ROOT/'research/observations.json').read_text())
  s=(ROOT/'experiments/period-search.html').read_text()
  self.assertEqual(d['source']['n_rows'],64814)
  self.assertEqual(d['source']['retained'],64713)
  for term in ('9.4874','305 ppm','411 ppm','18.973日',d['source']['git_blob_sha1']):
   self.assertIn(term,s)
  self.assertTrue(d['qualification']['posthoc'])
  self.assertFalse(d['qualification']['strictly_blind'])
  self.assertFalse(d['qualification']['exoplanet_new_discovery'])
 def test_false_positive_is_only_unverified_folder_label(self):
  d=json.loads((ROOT/'research/observations.json').read_text())
  self.assertEqual(d['challenge_sample']['repo_folder_label'],'false_positive')
  self.assertFalse(d['challenge_sample']['label_independently_verified'])
  self.assertFalse(d['qualification']['authoritative_false_positive_disposition_verified'])
 def test_release_excludes_research(self):
  from prepare_release import build
  import tempfile
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'dist';d=build('https://polymath-research-jp.onrender.com/',out)
   self.assertEqual(set(d['files']),{'index.html','social-card.png','experiments/kepler-227.html','experiments/period-search.html'})
   self.assertFalse((out/'research').exists())

if __name__=='__main__':unittest.main()
