# Create your views here.
from django.shortcuts import render, redirect
from sklearn.feature_extraction.text import HashingVectorizer
from nlp.forms import ReviewForm
import nlp.vectorizer as vect
import pickle
import os
import re
import numpy as np

######## Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'pkl_objects',
                 'classifier.pkl'), 'rb'))
stop = pickle.load(open(
                os.path.join(cur_dir, 
                'pkl_objects', 
                'stopwords.pkl'), 'rb'))


def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                           text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) \
                   + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

vect = HashingVectorizer(decode_error='ignore',
                         n_features=2**21,
                         preprocessor=None,
                         tokenizer=tokenizer)

def classify(document):
    label = {0: '부정', 1: '긍정'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba

def index(request):
    return render(request, 'nlp/input.html')

def predict(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data['review']
            label, proba = classify(document)
            returns = {'document' : document, 'label': label, 'rate': proba}
            return render(request, 'nlp/result.html', returns)  

