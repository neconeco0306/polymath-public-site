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
