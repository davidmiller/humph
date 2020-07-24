"""
Experimental parser for lead sheet notation
"""
import collections
import sys

from humph.finders import FINDERS
from humph.repertoire import Repertoire
from humph.utils import perc

def analyse(sheet=None):
    """
    Run all finders for either one lead sheet passed in, or all lead sheets
    """
    rep = Repertoire()
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
    print(f"{len(sheets)} songs ({corpus_length:,} beats):".rjust(26))
    results = [(name, perc(finder_length[name], corpus_length)) for name in finder_length]
    for name, p in sorted(results, key=lambda x: -x[1]):
        print(f"{name.rjust(25)}: {p:.2f}%")


def rank_for_finder():
    rep = Repertoire()
    rep.load()

    for finder in FINDERS:
        songs = rep.rank_for_finder(finder)

        print(f"\n\nTop 10 songs for {finder.name}")
        for summary in songs:
            print(f"{summary.leadsheet.title.rjust(25)}: {summary.percentage:.1f}%")


def main():
    rank_for_finder()
    return
    if len(sys.argv) > 1:
        analyse(sheet=" ".join(sys.argv[1:]))
    else:
        analyse()
    return


if __name__ == '__main__':
    main()
