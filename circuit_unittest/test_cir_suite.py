import unittest
import test_cir_method

suite = unittest.TestSuite()
loader = unittest.TestLoader()

suite.addTest(loader.loadTestsFromModule(test_cir_method))