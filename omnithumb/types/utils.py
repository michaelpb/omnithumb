from ..utils.graph import DirectedGraph

START = object() # just using as a unique symbol
def pair_looper(iterator):
    '''
    Loop through iterator yielding items in adjacent pairs
    '''
    left = START
    for item in iterator:
        if left is not START:
            yield (left, item)
        left = item
