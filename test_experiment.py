import unittest, re, json
from pathlib import Path
ROOT=Path(__file__).parent
class ExperimentTests(unittest.TestCase):
 def test_real_source_and_boundary(self):
  text=(ROOT/'experiments/kepler-227.html').read_text()
  self.assertIn('Kepler-227',text)
  self.assertIn('f7185dd055fc7993469bb788816be6f592751a38',text)
  self.assertIn('新惑星の発見ではありません',text)
  self.assertIn('元のMAST観測ファイルとのバイト単位の対応',text)
 def test_plot_data_are_fixed(self):
  text=(ROOT/'experiments/kepler-227.html').read_text()
  for key in ('b','wrong','c'):
   pattern= r'\b'+key+r':\[([0-9,\-]+)\]'
   m=re.search(pattern,text)
   self.assertIsNotNone(m,key)
   vals=[int(x) for x in m.group(1).split(',')]
   self.assertEqual(len(vals),160)
   self.assertLess(max(abs(x) for x in vals),1000)
  self.assertEqual([int(x) for x in re.search(r'\bb:\[([0-9,\-]+)\]',text).group(1).split(',')][79:81],[-519,-528])
 def test_links(self):
  s=(ROOT/'experiments/kepler-227.html').read_text()
  for url in ('https://science.nasa.gov/exoplanet-catalog/kepler-227-b/','https://exoplanetarchive.ipac.caltech.edu/overview/Kepler-227'):
   self.assertIn(url,s)
if __name__=="__main__":unittest.main()

class PeriodExperimentTests(unittest.TestCase):
 def test_new_period_experiment_evidence(self):
  s=(ROOT/'experiments/period-search.html').read_text()
  for term in ('FIELD EXPERIMENT 002','64,814','9.4874','411 ppm','305 ppm','2 / 120', '18.973日','厳格な盲検ではありません','新しい惑星を発見した','f7185dd055fc7993469bb788816be6f592751a38'):
   self.assertIn(term,s)
 def test_double_series_are_120(self):
  s=(ROOT/'experiments/period-search.html').read_text()
  for key in ('train','holdout'):
   m=re.search(key+r':\[([0-9,\-]+)\]',s)
   self.assertIsNotNone(m,key)
   vals=list(map(int,m.group(1).split(',')))
   self.assertEqual(len(vals),120)
  self.assertEqual(list(map(int,re.search(r'train:\[([0-9,\-]+)\]',s).group(1).split(',')))[13:15],[-485,-339])

 def test_mobile_chart_is_scrollable_and_dip_visible(self):
  s=(ROOT/'experiments/period-search.html').read_text()
  self.assertIn('class="chartscroll"',s)
  self.assertIn('.chartscroll svg{width:720px;max-width:none}',s)
  self.assertIn('function y(v){return 218-v*0.22}',s)
  self.assertTrue(all(40 <= 218-y*.22 <= 360 for y in (-526,-485,-339,0,125)))
 def test_site_has_entry_point(self):
  self.assertIn('experiments/period-search.html',(ROOT/'index.html').read_text())
