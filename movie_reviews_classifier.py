#%%
import copy
from sklearn.datasets import load_files
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
import numpy as np


def get_training_data(path):
    print("Loading Training Data...")
    logs_train = load_files(path)
    print(len(logs_train))

    text_train, y_train = logs_train.data, logs_train.target
    print('Classes', np.unique(y_train))

    return text_train, y_train
#%%
text_train, y_train = get_training_data('/Users/patila/PycharmProjects/NBCMovieReviews/data')
text_test, y_expec = get_training_data('/Users/patila/PycharmProjects/NBCMovieReviews/test')
print('Done')
#%%
# vector = CountVectorizer(analyzer='word', decode_error='ignore', max_features=65536)
vector = HashingVectorizer(n_features=2 ** 16, alternate_sign=False, analyzer='word', decode_error='ignore')

# tfidf_tranform = TfidfTransformer()

X_train = vector.fit_transform(text_train)
# X_train = tfidf_tranform.fit_transform(X_train, y_train)
X_test = vector.transform(text_test)
# X_test = tfidf_tranform.transform(X_test)

clf = RandomForestClassifier(n_jobs=-1, criterion='gini', n_estimators=300, warm_start=True)

clf.fit(X_train, y_train)
mod = copy.deepcopy(clf)

mod.estimators_ = clf.estimators_[200:]

y_preds = clf.predict(X_test)
acc = np.mean(y_preds == y_expec)
print('accuracy: ' + str(acc))
print(classification_report(y_preds, y_expec))

y2_preds = mod.predict(X_test)
acc = np.mean(y2_preds == y_expec)
print('accuracy: ' + str(acc))
print(classification_report(y2_preds, y_expec))

print('done')
