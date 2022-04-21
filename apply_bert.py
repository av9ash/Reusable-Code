from sklearn.base import BaseEstimator, TransformerMixin
from sentence_transformers import SentenceTransformer, util
import numpy as np


class BERTEncoder(TransformerMixin, BaseEstimator):
    """Wrapper for using annoy.AnnoyIndex as sklearn's KNeighborsTransformer"""

    def __init__(self, path):
        self.bert_model = SentenceTransformer(path)

    def fit(self, X):
        return self

    def transform(self, X):
        vectors = []
        for x in X:
            vectors.append(self.bert_model.encode(x, convert_to_tensor=False).tolist())
        return np.array(vectors)

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)
