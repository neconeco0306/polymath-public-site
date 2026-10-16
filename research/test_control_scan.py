import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from control_scan import run

class ChallengeControlTests(unittest.TestCase):
    def test_periodic_trough_does_not_mean_planet(self):
        period=7.0
        rows=[]
        for i in range(10000):
            t=i*.14
            y=10000*(1.0-.02*(.08<(t/period)%1<.095))
            rows.append((t,y))
        r=run(rows)
        self.assertGreater(r['raw_rows'],0)
        self.assertEqual(r['status'],'EXPLORATORY / NOT A PLANET CLASSIFIER')
        self.assertIn('planet',r['interpretation'])

if __name__=='__main__':unittest.main()
