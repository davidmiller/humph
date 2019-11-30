"""
Music utils

Utility functions and constants related to the domain
"""
from humph.utils import chunks

NOTES = [
    'A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'
]

ENHARMONICS = {
    'A#': 'Bb',
    'Db': 'C#',
    'D#': 'Eb',
    'Gb': 'F#',
    'G#': 'Ab'
}

P1 = 'Perfect Unison'
m2 = 'Semitone'
M2 = 'Whole Tone'
m3 = 'Minor Third'
M3 = 'Major Third'
P4 = 'Perfect Fourth'
TT = 'Tritone'
P5 = 'Perfect Fifth'
m6 = 'Minor Sixth'
M6 = 'Major Sixth'
m7 = 'Minor Seventh'
M7 = 'Major Seventh'
P8 = 'Perfect Octave'

INTERVALS = {
    0: P1,
    1: m2,
    2: M2,
    3: m3,
    4: M3,
    5: P4,
    6: TT,
    7: P5,
    8: m6,
    9: M6,
    10: m7,
    11: M7
}

def interval(a, b):
    """
    Return the interval between A and B
    """
    pos_a = NOTES.index(standard_enharmonics(a))
    pos_b = NOTES.index(standard_enharmonics(b))
    semitones = pos_b - pos_a
    if semitones <0:
        semitones += 12
    return INTERVALS[semitones]


def standard_enharmonics(n):
    """
    Return a standard enharmonic representation
    """
    if n in ENHARMONICS:
        return ENHARMONICS[n]
    return n

#
# Models
#
# Objects that model the domain
#

class Chord(object):
    """
    Object representing a single chord
    """

    def __init__(self, chord_string, duration):
        self._chord_string = chord_string

        # Set up initial properties
        self.root            = None
        self.duration        = duration #Beats
        self.extensions      = None

        # Qualities
        self.major           = False
        self.minor           = False
        self.dominant        = False
        self.half_diminished = False
        self.diminished      = False

        self._parse()

    def __repr__(self):
        return self._chord_string #+ (self.duration * '.')

    def _parse(self):
        """
        Parse the chord string and set properties on the object
        """
        ch = self._chord_string

        root_length = 1

        if ch[1] in ['b', '#']:
            root_length = 2
        self.root = ch[0:root_length]
        quality = ch[root_length:root_length+1]
        extensions = ch[root_length+1:]

        if quality in ['M', '6']:
            self.major = True

        if quality == '-':
            if ch[root_length:root_length+2] == '-M':
                self.minor_major = True
                extensions = ch[root_length+2:]
            else:
                self.minor = True

        if quality == '7':
            self.dominant = True

        if quality == '0':
            self.half_diminished = True

        if quality == 'o':
            self.diminished = True

        if extensions:
            self.extension = extensions

        return

    def enharmonic_root(self):
        """
        Return the standard enharmonic spelling of the root
        """
        return standard_enharmonics(self.root)


class Bar(object):
    """
    Object representing a single bar of music
    """
    def __init__(self, bar_string, timesig):
        self._bar_string = bar_string

        bar_beats = 4
        if timesig == '3/4':
            bar_beats = 3

        chord_strings = [c.strip() for c in self._bar_string.split(' ') if c]
        duration      = int(bar_beats / len(chord_strings))

        # Allow chords to be placed unevenly with . syntax
        chord_tuples = [(c, duration) for c in chord_strings]

        for i, chord_string in enumerate(chord_strings):
            if chord_string == '.':
                chord_tuples[i-1] = (chord_strings[i-1], duration*2)

        self.chords = [Chord(*c) for c in chord_tuples if c[0] != '.']

    def __repr__(self):
        return str(self.chords)

    def __iter__(self):
        def bar_generator():
            for chord in self.chords:
                yield chord
        return bar_generator()


class LeadSheet(object):
    """
    Object representing a lead sheet for a song
    """
    def __init__(self, leadsheet_string):
        self._leadsheet_string = leadsheet_string

        self.title   = None
        self.bars    = None
        self.beats   = None
        self.timesig = '4/4'

        self.parse()

    def parse(self):
        """
        Parse the raw string including shorcuts into Bars and Chords
        """

        # Metadata
        if '---' in self._leadsheet_string:
            meta, text = self._leadsheet_string.split('---')
            pairs = meta.split('\n')
            for pair in pairs:
                if pair.strip():
                    k, v = pair.split(':')
                    setattr(self, k.strip(), v.strip())
        else:
            text = self._leadsheet_string

        # Chords

        text = text.replace("\n", "")

        # Section repeats with { }
        if '{' in text:
            if '}' in text:
                start = text.index('{')
                end   = text.index('}')
                text  = text[0:start] + text[start+1:end] + text[start+1:end] + text[end+1:]

        # Section alterations with [ ]
        #
        # Warning - only allows 2 alterations
        #
        if text.count('[') == 4:
            splitted = text.split('[')
            new      = []
            new.append(splitted[0])
            new.append(splitted[1].replace(']', ''))
            new.append(splitted[2][splitted[2].index(']')+1:])
            new.append(splitted[4].replace(']', ''))
            text = "".join(new)

        # Bar repeats with %
        raw_bar_strings = [b.strip() for b in text.split('|') if b]
        bar_strings = []
        for i, barstring in enumerate(raw_bar_strings):
            if barstring != '%':
                bar_strings.append(barstring)
            else:
                # we go from bar strings not raw bar strings as sometimes (Modal)
                # the chord repeats for multiple bars so you need a previous bar
                # that has already been replaced
                bar_strings.append(bar_strings[i-1])

        self.bars = [Bar(b, self.timesig) for b in bar_strings]

        beats_per_bar = 4
        if self.timesig == '3/4':
            beats_per_bar = 3

        self.beats = len(self.bars) * beats_per_bar


    def __repr__(self):
        chords = "\n".join([str(l) for l in chunks(self.bars, 4)])
        if self.title:
            return f"{self.title}\n{chords}"
        return chords


    def __iter__(self):
        def leadsheet_generator():
            for bar in self.bars:
                yield bar

        return leadsheet_generator()
