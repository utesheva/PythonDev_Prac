import square
import unittest
import multiprocessing
import file
import time
import socket

class TestSrv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=file.main)
        cls.proc.start()
        time.sleep(1)    # Да, это костыль!
    
    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('hostanme', 1337))

    def test_0_srv(self):
        self.assertEqual(square.sqrootnet('5 3 2', self.s), "")

    def test_1_srv(self):
        self.assertEqual(square.sqrootnet('2 4 2', self.s), "1")

    def tearDown(self):
        self.s.close()

    @classmethod
    def tearDownClass(cls):
        cls.s.terminate()

