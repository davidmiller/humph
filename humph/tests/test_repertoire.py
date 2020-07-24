"""
Tests for humph.repertoire
"""
from unittest import TestCase

from humph import repertoire, songs, finders, music


class RepertoireTestCase(TestCase):

    def test_load(self):
        rep = repertoire.Repertoire()
        self.assertEqual(0, len(rep.songs))
        rep.load()
        self.assertGreater(len(rep.songs), 1)


    def test_filter(self):
        rep = repertoire.Repertoire()
        rep.load()

        monk = rep.filter(title="Blue Monk")
        self.assertEqual(1, len(monk))

        monk = monk[0]
        self.assertEqual("Blue Monk", monk.title)
        self.assertEqual(songs.BLUE_MONK, monk._leadsheet_string)

    def test_rank_for_finder(self):
        rep = repertoire.Repertoire()
        rep.songs = [music.LeadSheet(songs.TUNE_UP), music.LeadSheet(songs.ALL_BLUES)]

        ranked = rep.rank_for_finder(finders.Find251s)

        self.assertEqual(1, len(ranked))
