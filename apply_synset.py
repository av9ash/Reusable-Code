from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from collections import Counter
from scipy.sparse import csr_matrix
import json
from nltk.corpus import stopwords

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
              'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
              'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
              'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
              'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
              'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
              'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
              'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
              'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
              'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
              'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
              'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
              "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
              "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't",
              'wouldn', "wouldn't", 'behavior', 'error', 'file', 'il2', 'il4', 'interface', 'issue', 'juniper', 'junos',
              'log', 'name', 'net', 'pr', 'root', 'show', 'system', 'unexpected', 'version']


class SynsetTransformer(TransformerMixin, BaseEstimator):
    """Wrapper for using annoy.AnnoyIndex as sklearn's KNeighborsTransformer"""

    def __init__(self):
        with open('../data_extraction/embedding_clusters/synset2.json') as f:
            self.syn_set = json.loads(f.read())

        # This Vectorizer is only used to build vocab, and count frequencies
        self.cv = CountVectorizer(analyzer='word', decode_error='ignore', stop_words=stop_words)
        self.vocab = None
        self.index_to_head_map = {}
        self.tf_idf_transformer = TfidfTransformer()

    def fit(self, X):
        self.cv.fit(X)
        self.vocab = self.cv.vocabulary_.copy()

        for values in self.syn_set.values():
            features = values.copy()
            while features:
                head = features.pop()
                if head in self.vocab:
                    indx = self.vocab[head]
                    for feat in features:
                        if feat in self.vocab:
                            self.vocab[feat] = indx
                            self.index_to_head_map[indx] = head
        return self

    def _transform(self, X):
        sX = len(X)
        sY = len(self.vocab)
        row, col, val = [], [], []

        for idx, doc in enumerate(X):
            counts = self.cv.transform([doc]).toarray().sum(axis=0)
            count_word = dict(zip(self.cv.get_feature_names(), counts))
            # count_word = dict(Counter(doc.lower().split(' ')))

            for word, count in count_word.items():
                if word in self.vocab:
                    col_index = self.vocab.get(word)
                    if col_index >= 0:
                        row.append(idx)
                        col.append(col_index)
                        val.append(count)

        return csr_matrix((val, (row, col)), shape=(sX, sY)).toarray()

    def fit_transform(self, X, y=None):
        return self.tf_idf_transformer.fit_transform(self.fit(X)._transform(X)).toarray()

    def transform(self, X, y=None):
        return self.tf_idf_transformer.transform(self._transform(X)).toarray()

    # def fit_transform(self, X, y=None):
    #     return self.fit(X).transform(X)

    def inverse_transform(self, X):
        inverse_vocab = {}
        for word, index in self.vocab.items():
            inverse_vocab[index] = self.index_to_head_map.get(index, word)

        transformations = []
        for matrix in X:
            corpi = []
            for i, freq in enumerate(matrix):
                if freq > 0:
                    word = inverse_vocab[i]
                    corpi.append(word)
            transformations.append(corpi)

        return transformations


# st = SynsetTransformer()
# corpus = ['namerouting instanceterse verifycli',
#           'Guardian - MultiD: evo-pfemand is continuously coring with latest image']
# x = st.fit_transform(corpus)
# print(x)
# back_corpus = st.inverse_transform(x)
# print(back_corpus)
# print('done')
