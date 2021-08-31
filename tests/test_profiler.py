import unittest
import plogpro

import os


class DummyProfiler(plogpro.Profiler):
    def __init__(self):
        self.name = None
        self.start_time = None
        self.end_time = None
    def write(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time


class TestProfiler(unittest.TestCase):

    def test_instanciate_abc(self):
        self.assertRaises(TypeError, plogpro.Profiler)

    def test_write(self):
        p = DummyProfiler()

        self.assertIsNone(p.name)
        self.assertIsNone(p.start_time)
        self.assertIsNone(p.end_time)

        @p.profile
        def func():
            pass
        func()

        self.assertEqual(p.name, "func")
        self.assertIsNotNone(p.start_time)
        self.assertIsNotNone(p.end_time)
        self.assertGreaterEqual(p.end_time, p.start_time)


class TestTracingProfiler(unittest.TestCase):

    def setUp(self):
        self.fname = "profiler_test_output.json"

    def tearDown(self):
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def test_file_created(self):
        p = plogpro.TracingProfiler(self.fname)
        @p.profile
        def func():
            pass
        func()
        self.assertTrue(os.path.isfile(self.fname))
