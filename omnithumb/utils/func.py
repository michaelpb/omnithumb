class MemoizedFunction:
    '''
    Wraps a function and exposes a memoized interface
    '''
    def __init__(self, func):
        self.direct = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = (args, tuple(kwargs))
        if key in self.cache:
            return self.cache[key]
        value = self.direct(*args, **kwargs)
        self.cache[key] = value
        return value

    def clear_memoized(self):
        self.cache = {}


def memoize(f):
    """
	Memoization decorator for functions taking one or more arguments.
	"""
    return MemoizedFunction(f)

