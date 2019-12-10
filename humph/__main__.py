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
    Run all finders for either one lead sheet passed in, or all lead sheets
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

        leadsheet_summaries = []

        for finder in FINDERS:
            f = finder(leadsheet)
            summary = f.run()
            leadsheet_summaries.append(summary)
            finder_length[summary.name] += summary.duration

        for summary in reversed(sorted(leadsheet_summaries, key=lambda x: x.percentage)):
            if summary.count > 0:
                print(summary)

    if len(sheets) == 1:
        return

    # Global Finder Summary
    print(30*'^')
    print(f"{len(sheets)} songs:")
    results = [(name, perc(finder_length[name], corpus_length)) for name in finder_length]
    for name, p in sorted(results, key=lambda x: -x[1]):
        print(f"{name}: {p:.2f}%")


def rank_for_finder():
    from humph.finders import Find25s as finder

    rep = Repertiore()
    rep.load()

    songs = rep.rank_for_finder(finder)
    for song in songs:
        print(song)


def main():
    if len(sys.argv) > 1:
        analyse(sheet=" ".join(sys.argv[1:]))
    else:
        analyse()
    return


if __name__ == '__main__':
    main()
