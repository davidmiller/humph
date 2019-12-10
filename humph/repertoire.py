"""
Represent the standard repertoire
"""
from humph.music import LeadSheet
from humph import songs


class Repertiore(object):
    """
    Single object containing the standard repertoire
    """

    def __init__(self):
        """
        Set initial self. values
        """
        self.songs = []

    def load(self):
        """
        Load the repertoire into leadsheet objects
        """
        self.songs = []
        for raw in dir(songs):
            if raw.startswith('__'):
                continue
            self.songs.append(LeadSheet(getattr(songs,raw)))
        return

    def filter(self, **kwargs):
        """
        Filter the standard repertoire according to KWARGS
        """
        filtered = []
        for s in self.songs:
            if all([getattr(s, k) == kwargs[k] for k in kwargs]):
                filtered.append(s)

        return filtered


    def rank_for_finder(self, finder):
        """
        Given a FINDER, rank all songs in the repertoire by the
        % they are comprised sequecnes matching FINDER
        """
        return []
