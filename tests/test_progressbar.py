import unittest
import plogpro


class DummyProgressBar(plogpro.ProgressBar):
    def draw(self):
        pass


class TestProgressBar(unittest.TestCase):

    def setUp(self):
        self.nsteps = 5
        self.p = DummyProgressBar(self.nsteps)

    def test_instanciate_abc(self):
        self.assertRaises(TypeError, plogpro.ProgressBar, self.nsteps)

    def test_nsteps(self):
        self.assertEqual(self.p.nsteps, self.nsteps)
    
    def test_progress(self):
        self.assertAlmostEqual(self.p.progress(), 0.0)
        for i in range(self.nsteps):
            self.p.update()
            self.assertAlmostEqual(self.p.progress(), (i+1) / self.nsteps)

    def test_step_increment(self):
        self.assertEqual(self.p.step, 0)
        for i in range(self.nsteps):
            self.p.update()
            self.assertEqual(self.p.step, (i+1))

    def test_step_select(self):
        self.assertEqual(self.p.step, 0)
        self.p.update(self.nsteps)
        self.assertEqual(self.p.step, self.nsteps)


class TestConsoleProgressBar(unittest.TestCase):

    def test_init(self):
        nsteps = 100
        width = 70
        cpb = plogpro.ConsoleProgressBar(nsteps, width)
        self.assertEqual(cpb.nsteps, nsteps)
        self.assertEqual(cpb.width, width)
    
    def test_no_errors(self):
        # Check if no errors are raised while using the progressbar
        nsteps = 100
        cpb = plogpro.ConsoleProgressBar(nsteps)
        for _ in range(nsteps):
            cpb.update()
