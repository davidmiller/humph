"""
Unittests for humph.utils
"""
from unittest import TestCase

from humph import utils


class ChunksTestCase(TestCase):

    def test_chunks(self):
        iterable = [1,2,3,4,5,5]
        out      = [[1,2], [3,4], [5,5]]
        self.assertEqual(out, list(utils.chunks(iterable, 2)))


class PercTestCase(TestCase):

    def test_perc(self):
        part  = 20
        whole = 200
        self.assertEqual(10, utils.perc(20, 200))
