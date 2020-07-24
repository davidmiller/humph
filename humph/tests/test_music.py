"""
Unittests for humph.music
"""
import unittest

from humph import music


class IntervalTestCase(unittest.TestCase):

    def test_interval(self):
        self.assertEqual('Perfect Fourth', music.interval('C', 'F'))

    def test_interval_crosses_octave(self):
        self.assertEqual('Major Third', music.interval('G', 'B'))


class StandardEnharmonicsTestCase(unittest.TestCase):

    def test_stanardise_enharmonic(self):
        self.assertEqual('Bb', music.standard_enharmonics('A#'))


class ChordTestCase(unittest.TestCase):

    def test_init(self):
        chord = music.Chord('Bb', 1)
        self.assertEqual(1, chord.duration)

    def test_repr(self):
        chord = music.Chord('C-', 1)
        self.assertEqual('C-', chord.__repr__())

    def test_root(self):
        chord = music.Chord('F', 1)
        self.assertEqual('F', chord.root)

    def test_sharp_root(self):
        chord = music.Chord('F#', 1)
        self.assertEqual('F#', chord.root)

    def test_flat_root(self):
        chord = music.Chord('Eb', 1)
        self.assertEqual('Eb', chord.root)

    def test_bass_note(self):
        chord = music.Chord('C/E', 1)
        self.assertEqual('E', chord.bass_note)

    def test_bass_note_seventh(self):
        chord = music.Chord('C7/E', 1)
        self.assertEqual('E', chord.bass_note)

    def test_bass_note_seventh_chord_with_extensions(self):
        chord = music.Chord('C7b9#11/E', 1)
        self.assertEqual('E', chord.bass_note)

    def test_major(self):
        chord = music.Chord('CM7', 1)
        self.assertTrue(chord.major)

    def test_minor(self):
        chord = music.Chord('C-7', 1)
        self.assertTrue(chord.minor)

    def test_minor_major(self):
        chord = music.Chord('C-M7', 1)
        self.assertTrue(chord.minor_major)

    def test_dominant(self):
        chord = music.Chord('C7', 1)
        self.assertTrue(chord.dominant)

    def test_half_diminished(self):
        chord = music.Chord('C0', 1)
        self.assertTrue(chord.half_diminished)

    def test_diminished(self):
        chord = music.Chord('Co', 1)
        self.assertTrue(chord.diminished)

    def test_extensions(self):
        chord = music.Chord('C7b9', 1)
        self.assertEqual('b9', chord.extension)

    def test_enharmonic_root(self):
        chord = music.Chord('Db7', 1)
        self.assertEqual('C#', chord.enharmonic_root())


class BarTestCase(unittest.TestCase):

    def test_bar_sets_duration(self):
        bar = music.Bar('C-7', '4/4')
        self.assertEqual(4, bar.chords[0].duration)

    def test_bar_sets_duration_3_4(self):
        bar = music.Bar('C-7', '3/4')
        self.assertEqual(3, bar.chords[0].duration)

    def test_bar_sets_duration_equally(self):
        bar = music.Bar('C-7 G7', '4/4')
        self.assertEqual(2, bar.chords[0].duration)

    def test_dot_syntax_allows_uneven_duration(self):
        bar = music.Bar('CM7 . C-7 F7', '4/4')
        self.assertEqual(2, bar.chords[0].duration)
        self.assertEqual(1, bar.chords[1].duration)
        self.assertEqual(1, bar.chords[2].duration)

    def test_repr(self):
        bar = music.Bar('C-7', '4/4')
        self.assertEqual('[C-7]', bar.__repr__())

    def test_iter(self):
        bar = music.Bar('C-7 F7 Bb7 .', '4/4')
        for i, chord in enumerate(bar):
            self.assertEqual(chord, bar.chords[i])


class LeadSheetTestCase(unittest.TestCase):

    def test_default_timesig(self):
        raw = "A-7 | D7 | G7"
        sheet = music.LeadSheet(raw)
        self.assertEqual('4/4', sheet.timesig)

    def test_set_beats(self):
        raw = "A-7 | D7 | G7"
        sheet = music.LeadSheet(raw)
        self.assertEqual(12, sheet.beats)

    def test_timesig_set(self):
        raw = """
        timesig: 3/4
        ---
        A-7 | D7 | G7
        """
        sheet = music.LeadSheet(raw)
        self.assertEqual('3/4', sheet.timesig)

    def test_title_set(self):
        raw = """
        title: Dominant Cycle
        ---
        A7 | D7 | G7
        """
        sheet = music.LeadSheet(raw)
        self.assertEqual('Dominant Cycle', sheet.title)

    def test_expands_section_repeats(self):
        raw = "{ D-7 | G7 | CM7 | % |}"
        sheet = music.LeadSheet(raw)
        self.assertEqual(8, len(list([k for k in sheet])))

    def test_expands_repeats_with_alternate_blocks(self):
        raw = "{ D-7 | G7 | CM7 | [ % ][ E-7 A7 ]|}"
        sheet = music.LeadSheet(raw)
        self.assertEqual('C', sheet.bars[3].chords[0].root)
        self.assertEqual('E', sheet.bars[7].chords[0].root)
        self.assertEqual('A', sheet.bars[7].chords[1].root)

    def test_expands_repeats(self):
        raw = "B-7 | % |"
        sheet = music.LeadSheet(raw)
        self.assertEqual('B', sheet.bars[1].chords[0].root)

    def test_expands_successive_repeats(self):
        raw = "A-7 | % | % |"
        sheet = music.LeadSheet(raw)
        self.assertEqual('A', sheet.bars[2].chords[0].root)

    def test_repr(self):
        raw = """
        title: Dominant Cycle
        ---
        A7 | D7  | G7  | C7
        F7 | Bb7 | Eb7 | Ab7
        """

        expected = """Dominant Cycle
[[A7], [D7], [G7], [C7, F7]]
[[Bb7], [Eb7], [Ab7]]"""

        sheet = music.LeadSheet(raw)

        self.assertEqual(expected, sheet.__repr__())

    def test_repr_no_title(self):
        raw = """
        A7 | D7  | G7  | C7
        F7 | Bb7 | Eb7 | Ab7
        """

        expected = """[[A7], [D7], [G7], [C7, F7]]
[[Bb7], [Eb7], [Ab7]]"""

        sheet = music.LeadSheet(raw)

        self.assertEqual(expected, sheet.__repr__())
