"""
Experimental parser for lead sheet notation
"""
import collections
import sys

from humph.finders import FINDERS
from humph.repertoire import Repertiore
from humph.utils import perc

def analyse(sheet=None):
    """
    Run selected finders for sheets
    """
    rep = Repertiore()
    rep.load()

    sheets = rep.songs
    if sheet:
        sheets = rep.filter(title=sheet)

    corpus_length = 0
    finder_length = collections.defaultdict(int)

    for leadsheet in sheets:

        print(leadsheet)

        corpus_length += leadsheet.beats

        for finder in FINDERS:
            f = finder(leadsheet)
            summary = f.run()
            finder_length[summary.name] += summary.duration
            print(summary)

    if len(sheets) == 1:
        return

    # Global summary
    print(30*'^')
    print(f"{len(sheets)} songs:")
    for name in finder_length:
        p = perc(finder_length[name], corpus_length)
        print(f"{name}: {p}%")


def main():
    if len(sys.argv) > 1:
        analyse(sheet=" ".join(sys.argv[1:]))
    else:
        analyse()
    return


if __name__ == '__main__':
    main()
