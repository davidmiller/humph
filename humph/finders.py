"""
Finders = analysing sequences
"""
import itertools

from humph.music import interval, P1, m2, M2, m3, M3, P4, TT, P5, m6, M6, m7, M7, P8
from humph.utils import perc

# TODO:
#
# Minor 2-5
# 6-2-5-1
# I7 - IV7 (Blues movement)
# II - V - 17 (1dominant rather than minor )
# I7 - VI - II - V (dominant 1 - maybe incorporate into 1-6-2-5?)
# Dominant up half step and diminished


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

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 2)
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

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 2)
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

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 3)

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

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 4)

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

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 4)

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


class FindMinor251s(Finder):
    """
    Find occurrences of the minor ii-V progression in this lead sheet
    """
    name = 'minor 2-5-1s'

    def find(self):
        """
        Returns count, instanecs
        """
        count = 0
        instances = []

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 3)

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

        chords = [c for bar in self.leadsheet for c in bar]

        chord_sequences = sequences(chords, 2)

        for sequence in chord_sequences:
            if sequence[0].major:
                if sequence[1].minor:
                    if sequence[0].enharmonic_root() == sequence[1].enharmonic_root():
                        count += 1
                        instances.append(sequence)

        return count, instances


FINDERS = [
    Find251s,
    Find25s,
    Find51s,
    Find1625s,
    Find3625s,
    FindMinor251s,
    FindMajorParallelMinor,
]
