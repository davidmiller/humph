"""
Tests for humph.repertoire
"""
from unittest import TestCase

from humph import repertoire, songs


class RepertioreTestCase(TestCase):

    def test_load(self):
        rep = repertoire.Repertiore()
        self.assertEqual(0, len(rep.songs))
        rep.load()
        self.assertGreater(len(rep.songs), 1)


    def test_filter(self):
        rep = repertoire.Repertiore()
        rep.load()

        monk = rep.filter(title="Blue Monk")
        self.assertEqual(1, len(monk))

        monk = monk[0]
        self.assertEqual("Blue Monk", monk.title)
        self.assertEqual(songs.BLUE_MONK, monk._leadsheet_string)
