"""
Utils - generic functions to manipulate datastructures

No domain specific logic
"""

def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def perc(part, whole):
    """
    Return PART as a percentage of WHOLE to the nearest integer
    """
    return int(100 * float(part)/float(whole))
