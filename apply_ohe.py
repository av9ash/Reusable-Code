from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
import numpy as np
from scipy import sparse


class Platform_OHE(TransformerMixin, BaseEstimator):
    """Wrapper for using annoy.AnnoyIndex as sklearn's KNeighborsTransformer"""

    def __init__(self):
        self.vocab = {}

    def fit(self, X):
        values = []
        for item in X:
            values += item.split(':')

        all_features = set(values)
        self.vocab = {feature: i for i, feature in enumerate(all_features)}

        return self

    def transform(self, X):
        n_features = len(self.vocab.keys())
        encodings = np.array([[0] * n_features for _ in range(len(X))])
        for i, text in enumerate(X):
            for feature in text.split(':'):
                idx = self.vocab.get(feature)
                encodings[i][idx] = 1
        return sparse.csr_matrix(encodings)

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)


# texts = ['acx:all-junos:mx/x:ptx-series:srx-series:wrlinux', 'all-evo:all-junos:evo-ptx-series',
#          'evo-acx-series:evo-ptx-series:evo-ptx-series:ptx-series',
#          'all-evo:all-junos:evo-ptx-series:mx/x:mx/x:ptx-series', 'evo-ptx-series:ex-series:mx/x',
#          'evo-ptx-series:ptx-series']
#
# pt_hot = Platform_OHE()
# pt_hot.fit(texts)
# t = pt_hot.transform(texts)
# print(t.toarray())
# print('done')
