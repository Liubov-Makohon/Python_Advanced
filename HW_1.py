import collections
from heapq import nsmallest
from operator import itemgetter
import functools


def cache(max_limit=5):
    def internal(f):
        @functools.wraps(f)
        def deco(*args):
            use_count[args] += 1
            if args in deco._cache:
                return deco._cache[args]
            result = f(*args)
            deco._cache[args] = result
            if len(deco._cache) >= max_limit:
                for key, _ in nsmallest(1, use_count.items(), key=itemgetter(1)):
                    del deco._cache[key], use_count[key]
            return result
        deco._cache = collections.OrderedDict()
        use_count = collections.Counter()
        return deco
    return internal

