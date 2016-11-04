"""
Unit tests for lib.py

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""
import unittest

from doj.lib import get_map


class DojTest(unittest.TestCase):

    def test_get_map(self):
        return_dict = get_map()
        self.assertTrue('nodes' in return_dict)
        self.assertTrue('inferences' in return_dict)
        self.assertTrue('undercuts' in return_dict)
