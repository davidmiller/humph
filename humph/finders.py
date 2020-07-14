"""
Finders = analysing sequences
"""
import itertools

from humph.music import Chord, interval, P1, m2, M2, m3, M3, P4, TT, P5, m6, M6, m7, M7, P8
from humph.utils import perc

# TODO:
#
# II - V - 17 (1dominant rather than minor )
# I7 - VI - II - V (dominant 1 - maybe incorporate into 1-6-2-5?)
# Dominant up half step and diminished
# What happens after the tonic ?


def sequences(iterable, n):
    """
    Recursively provide all sequences of length N in ITERABLE
    """
    parts = []
    start = 0
    for i in range(len(iterable)):
        sequence = iterable[i:i+n]
        if len(sequence) == n:
            # sometimes python list slicing will give you a trailing single instance
            parts.append(sequence)
        start += 1
    return parts


class FinderSummary(object):

    def __repr__(self):
        return self.summary

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


class Finder(object):
    """
    Utility class to locate sequences in leadsheets
    """
    def __init__(self, leadsheet):

        self.leadsheet = leadsheet

    def find(self):
        """
        Find functions look for particular chord sequences
        in a lead sheet. They return a tuple of
        (COUNT, INSTANCES)
        """
        pass

    def sequences_of(self, length):
        """
        return sequences of chords in SELF.LEADSHEET of length LENGTH

        - Turn the leadsheet into a sequence that includes the turnaround
        - Drop duplicate chords e.g. a two D-7 chords for two bars in 4/4
          becomes one D-7 chord of duration 8 beats
        """
        chords = [c for bar in self.leadsheet for c in bar]
        chords += chords[:length-1]

        collapsed = []

        for chord in chords:

            if len(collapsed) == 0:
                collapsed.append(chord)
                continue

            if chord._chord_string == collapsed[-1]._chord_string:
                collapsed[-1] = Chord(chord._chord_string, chord.duration+collapsed[-1].duration)
                continue

            collapsed.append(chord)

        return sequences(collapsed, length)

    def run(self):
        """
        Run the finder, and return a FinderSummary of
        COUNT, INSTANCEs, PERCENTAGE, SUMMARY_STRING
        """
        count, instances = self.find()
        duration = sum([c.duration for c in itertools.chain(*instances)])
        p = perc(duration, self.leadsheet.beats)
        summary_string = f"{count} {self.name} ({p}%)"
        return FinderSummary(
            count=count, summary=summary_string, percentage=p, instances=instances,
            leadsheet=self.leadsheet, duration=duration, name=self.name
        )


class Find25s(Finder):
    """
    Find ocurrences of the ii-V progression in this lead sheet
    """
    name = '2-5s'

    def find(self):
        """
        Returns count, instances
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(2)
        for sequence in chord_sequences:
            if sequence[0].minor:
                if sequence[1].dominant:
                    the_interval = interval(sequence[0].root, sequence[1].root)
                    if the_interval == P4:
                        count += 1
                        instances.append(sequence)

        return count, instances


class Find51s(Finder):
    """
    Find ocurrences of the ii-V progression in this lead sheet
    """
    name = '5-1s'

    def find(self):
        """
        Returns count, instances
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(2)
        for sequence in chord_sequences:
            if sequence[0].dominant:
                if sequence[1].major:
                    the_interval = interval(sequence[0].root, sequence[1].root)
                    if the_interval == P4:
                        count += 1
                        instances.append(sequence)

        return count, instances


class Find251s(Finder):
    """
    Find occurrences of the ii-V-I progression in this lead sheet
    """
    name = '2-5-1s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(3)

        for sequence in chord_sequences:
            if sequence[0].minor:
                if sequence[1].dominant:
                    if sequence[2].major: # It's minor, dominant seventh, check intervals

                        interval1 = interval(sequence[0].root, sequence[1].root)
                        interval2 = interval(sequence[1].root, sequence[2].root)

                        if interval1 == P4:
                            if interval2 == P4:
                                count += 1
                                instances.append(sequence)

        return count, instances




class Find25I7s(Finder):
    """
    Find occurrences of the ii-V-I7 progression in this lead sheet
    """
    name = 'ii-V-I7'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(3)

        for sequence in chord_sequences:
            if sequence[0].minor:
                if sequence[1].dominant:
                    if sequence[2].dominant: # It's minor, dominant seventh, dominant seventh, check intervals

                        interval1 = interval(sequence[0].root, sequence[1].root)
                        interval2 = interval(sequence[1].root, sequence[2].root)

                        if interval1 == P4:
                            if interval2 == P4:
                                count += 1
                                instances.append(sequence)

        return count, instances




class Find1625s(Finder):
    """
    Find occurrences of the I-VI-II-V progression in this lead sheet
    """
    name = '1-6-2-5s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(4)

        for sequence in chord_sequences:
            if sequence[0].major:
                if sequence[1].minor or sequence[1].dominant:
                    if sequence[2].minor: # It's major, minor, minor, dominant, check intervals
                        if sequence[3].dominant:

                            interval1 = interval(sequence[0].root, sequence[1].root)
                            interval2 = interval(sequence[1].root, sequence[2].root)
                            interval3 = interval(sequence[2].root, sequence[3].root)

                            if interval1 == M6:
                                if interval2 == P4:
                                    if interval3 == P4:
                                        count += 1
                                        instances.append(sequence)

        return count, instances



class Find3625s(Finder):
    """
    Find occurrences of the III-VI-II-V progression in this lead sheet
    """
    name = '3-6-2-5s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(4)

        for sequence in chord_sequences:
            if sequence[0].minor:
                if sequence[1].minor or sequence[1].dominant:
                    if sequence[2].minor: # It's major, minor, minor, dominant, check intervals
                        if sequence[3].dominant:

                            interval1 = interval(sequence[0].root, sequence[1].root)
                            interval2 = interval(sequence[1].root, sequence[2].root)
                            interval3 = interval(sequence[2].root, sequence[3].root)

                            if interval1 == P4:
                                if interval2 == P4:
                                    if interval3 == P4:
                                        count += 1
                                        instances.append(sequence)

        return count, instances


class Find6251s(Finder):
    """
    Find occurrences of the VI-II-V-I progression in this lead sheet
    """
    name = '6-2-5-1s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(4)

        for sequence in chord_sequences:
            if sequence[0].minor:
                if sequence[1].minor:
                    if sequence[2].dominant: # It's major, minor, minor, dominant, check intervals
                        if sequence[3].major:

                            interval1 = interval(sequence[0].root, sequence[1].root)
                            interval2 = interval(sequence[1].root, sequence[2].root)
                            interval3 = interval(sequence[2].root, sequence[3].root)

                            if interval1 == P4:
                                if interval2 == P4:
                                    if interval3 == P4:
                                        count += 1
                                        instances.append(sequence)

        return count, instances


class FindMinor251s(Finder):
    """
    Find occurrences of the minor ii-V-i progression in this lead sheet
    """
    name = 'minor 2-5-1s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(3)

        for sequence in chord_sequences:
            if sequence[0].half_diminished:
                if sequence[1].dominant:
                    if sequence[2].minor: # It's 0 7 -, check intervals

                        interval1 = interval(sequence[0].root, sequence[1].root)
                        interval2 = interval(sequence[1].root, sequence[2].root)

                        if interval1 == P4:
                            if interval2 == P4:
                                count += 1
                                instances.append(sequence)

        return count, instances


class FindMinor25s(Finder):
    """
    Find occurrences of the minor ii-V progression in this lead sheet
    """
    name = 'minor 2-5s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(2)

        for sequence in chord_sequences:
            if sequence[0].half_diminished:
                if sequence[1].dominant:

                        interv = interval(sequence[0].root, sequence[1].root)

                        if interv == P4:
                            count += 1
                            instances.append(sequence)

        return count, instances


class FindMajorParallelMinor(Finder):
    """
    Find occurrences of the Major to Parrallel Minor cadence
    """
    name = 'Major-Parallel Minor'

    def find(self):
        """
        returns count, instances
        """
        count = 0
        instances = []

        chord_sequences = self.sequences_of(2)

        for sequence in chord_sequences:
            if sequence[0].major:
                if sequence[1].minor:
                    if sequence[0].enharmonic_root() == sequence[1].enharmonic_root():
                        count += 1
                        instances.append(sequence)

        return count, instances


class FindSearsRoebuckBridges(Finder):
    """
    Find occurrences of the Sears Roebuck bridge
    """
    name = "Sears Roebuck"

    def find(self):
        """
        returns count, instances
        """
        count = 0
        instances = []
        chord_sequences = self.sequences_of(4)
        for sequence in chord_sequences:
            if [c for c in sequence if not c.dominant]:
                continue

            # Do they move in fourths?
            interval1 = interval(sequence[0].root, sequence[1].root)
            interval2 = interval(sequence[1].root, sequence[2].root)
            interval3 = interval(sequence[2].root, sequence[3].root)

            if interval1 == P4 and interval2 == P4 and interval3 == P4:
                count += 1
                instances.append(sequence)

        return count, instances


class FindI7IV7Movements(Finder):
    """
    Find occurrences of I7 - IV7 ("Blues" movement, dominants in fourths)
    """
    name = "I7-IV7"

    def find(self):
        """
        Returns count, instances
        """
        count     = 0
        instances = []
        chord_sequences = self.sequences_of(2)
        for sequence in chord_sequences:
            if sequence[0].dominant and sequence[1].dominant:
                if interval(sequence[0].root, sequence[1].root) == P4:
                    count += 1
                    instances.append(sequence)

        return count, instances


class FindMinor7Minor251of5(Finder):
    """
    Find occurrences of G-7 G-7/F | E07 A7b9 | D-7
    """
    name = "-7 -7/7 Minor 251 of 5"

    def find(self):
        """
        Returns count, instances
        """
        count     = 0
        instances = []

        chord_sequences = self.sequences_of(5)

        for sequence in chord_sequences:
            # Frist bar is e.g. C-7 C-7/Bb
            if sequence[0].minor:
                if sequence[0].root == sequence[1].root:
                    if sequence[1].bass_note:
                        if interval(sequence[0].root, sequence[1].bass_note) == m7:
                            # bars 2&3 are a minor 251 of 5
                            interval1 = interval(sequence[0].root, sequence[2].root)
                            interval2 = interval(sequence[2].root, sequence[3].root)
                            interval3 = interval(sequence[3].root, sequence[4].root)
                            if sequence[2].half_diminished:
                                if sequence[3].dominant:
                                    if sequence[4].minor:
                                        if  interval1 == M6:
                                            if interval2 == P4:
                                                if interval3 == P4:

                                                    count += 1
                                                    instances.append(sequence)
        return count, instances



FINDERS = [
    Find251s,
    Find25I7s,
    Find25s,
    Find51s,
    Find1625s,
    Find3625s,
    Find6251s,
    FindMinor251s,
    FindMinor25s,
    FindMajorParallelMinor,
    FindSearsRoebuckBridges,
    FindI7IV7Movements,
    FindMinor7Minor251of5,
]
