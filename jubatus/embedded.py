__all__ = [
    'Anomaly',
    'Bandit',
    'Burst',
    'Classifier',
    'Clustering',
    'NearestNeighbor',
    'Recommender',
    'Regression',
    'Stat',
    'Graph',
    'Weight',
]

class _EmbeddedUnavailable(object):
    def __init__(self, *args, **kwargs):
        raise RuntimeError('Embedded Jubatus Python module is not installed.')

try:
    from embedded_jubatus import Anomaly
    from embedded_jubatus import Bandit
    from embedded_jubatus import Burst
    from embedded_jubatus import Classifier
    from embedded_jubatus import Clustering
    from embedded_jubatus import NearestNeighbor
    from embedded_jubatus import Recommender
    from embedded_jubatus import Regression
    from embedded_jubatus import Stat
    from embedded_jubatus import Weight
    from embedded_jubatus import Graph
except ImportError:
    Anomaly = _EmbeddedUnavailable
    Bandit = _EmbeddedUnavailable
    Burst = _EmbeddedUnavailable
    Classifier = _EmbeddedUnavailable
    Clustering = _EmbeddedUnavailable
    NearestNeighbor = _EmbeddedUnavailable
    Recommender = _EmbeddedUnavailable
    Regression = _EmbeddedUnavailable
    Stat = _EmbeddedUnavailable
    Graph = _EmbeddedUnavailable
    Weight = _EmbeddedUnavailable
