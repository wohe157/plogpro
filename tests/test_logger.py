import unittest
import plogpro

import os
from datetime import datetime


class DummyLogger(plogpro.Logger):
    def __init__(self):
        self.msg = None
    def write_message(self, msg):
        self.msg = msg


class TestLogMessage(unittest.TestCase):

    def setUp(self):
        self.msg = "Test message"
        self.type = plogpro.LogType.INFO

    def test_init(self):
        instance = plogpro.LogMessage(self.msg, self.type)
        self.assertEqual(instance.msg, self.msg)
        self.assertEqual(instance.type, self.type)
        self.assertIsInstance(instance.time, datetime)

    def test_all_types(self):
        for msg_type in plogpro.LogType:
            with self.subTest(msg_type=msg_type):
                instance = plogpro.LogMessage(self.msg, msg_type)
                self.assertEqual(instance.type, msg_type)

    def test_wrong_message(self):
        self.assertRaises(ValueError, plogpro.LogMessage, 1, self.type)

    def test_wrong_type(self):
        self.assertRaises(ValueError, plogpro.LogMessage, self.msg, 1)

    def test_time(self):
        t = datetime.now()
        instance = plogpro.LogMessage(self.msg, self.type)
        self.assertGreater(instance.time, t)
        self.assertLess(instance.time, datetime.now())


class TestLogger(unittest.TestCase):

    def setUp(self):
        self.msg = "Test message"

    def test_instanciate_abc(self):
        self.assertRaises(TypeError, plogpro.Logger, self.msg)

    def test_log(self):
        l = DummyLogger()
        self.assertIsNone(l.msg)
        l.log(self.msg)
        self.assertEqual(l.msg.msg, self.msg)


class TestTextLogger(unittest.TestCase):

    def setUp(self):
        self.fname = "logger_test_output.log"

    def tearDown(self):
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def test_no_errors(self):
        l = plogpro.TextLogger(self.fname)
        l.log("Test message")

    def test_logfile_created(self):
        l = plogpro.TextLogger(self.fname)
        os.path.isfile(self.fname)


class TestConsoleLogger(unittest.TestCase):

    def test_no_errors(self):
        l = plogpro.ConsoleLogger()
        l.log("Test message")
