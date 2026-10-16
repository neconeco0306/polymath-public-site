import unittest, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from period_search import git_sha1, fold, evaluate, detrend, grid

class PeriodSearchTests(unittest.TestCase):
    def test_git_blob_identity(self):
        self.assertEqual(git_sha1(b'hello\n'),'ce013625030ba8dba906f756967f9e9ca394464a')
    def test_detrending_unity_series(self):
        data=[(float(i)/4, 100.0) for i in range(100)]
        self.assertEqual(len(detrend(data)),len(data))
        self.assertTrue(all(v==0 for _,v in detrend(data)))
    def test_synthetic_detect_and_negative(self):
        p=4.75
        rows=[]
        for i in range(40000):
            t=i*.043
            phase=(t/p) % 1
            signal = -900 if (.185 < phase < .199) else 0
            noise = 45*((i*37)%17-8)/8
            rows.append((t,signal+noise))
        hit=evaluate(p,rows,0)
        self.assertGreater(hit['depth_ppm'], 300)
        self.assertGreater(hit['n'], 160)
        bad=evaluate(4.5,rows,0)
        self.assertGreater(hit['depth_ppm'],bad['depth_ppm']*2)
    def test_fixed_phase_holdout(self):
        rows=[(i*.05,-800 if .11<((i*.05/4.75)%1)<.128 else 0) for i in range(30000)]
        a=evaluate(4.75,rows[:15000],0)
        b=evaluate(4.75,rows[15000:],0,chosen=a['bin'])
        self.assertGreater(b['depth_ppm'],100)
    def test_grid_finds_approx_period(self):
        rows=[(i*.11,-650 if .09<((i*.11/4.75)%1)<.107 else 0) for i in range(18000)]
        top=grid(4.6,4.9,.002,rows,0)[:10]
        self.assertTrue(any(abs(v['period']-4.75)<.005 for v in top))

if __name__=='__main__':unittest.main()
