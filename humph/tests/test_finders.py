"""
Unittests for humph.finders
"""
import unittest

from humph import music

from humph import finders


class FinderSummaryTestCase(unittest.TestCase):

    def test_repr(self):
        fsum = finders.FinderSummary(summary='wat')
        self.assertEqual('wat', fsum.__repr__())


class FinderTestCase(unittest.TestCase):

    def test_find(self):

        finder = finders.Finder(None)

        with self.assertRaises(NotImplementedError):
            finder.find()


class Find25sTestCase(unittest.TestCase):

    def test_find(self):
        sheet = music.LeadSheet("E-7 A7 | A-7 D7 | D-7 G7 | CM7 ")

        finder = finders.Find25s(sheet)

        count, instances = finder.find()

        self.assertEqual(3, count)


class Find51s(unittest.TestCase):
    def test_find(self):
        sheet = music.LeadSheet("E-7 A7 | A-7 D7 | D-7 G7 | CM7 ")

        finder = finders.Find51s(sheet)

        count, instances = finder.find()

        self.assertEqual(1, count)
