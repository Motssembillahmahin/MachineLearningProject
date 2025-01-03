# -*- coding: utf-8 -*-
"""FakeNewsChecking.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a4QAP-9h4u6zKIvK43YkWVdakJ_rtZ0Q
"""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

# printing the stopwords in English
print(stopwords.words('english'))

"""Data Preprocessing"""

import pandas as pd

# Attempt to read the CSV file, handling potential errors
try:
    dataset = pd.read_csv('/content/train.csv', engine='python')
except pd.errors.ParserError:
    # If ParserError occurs, try specifying 'error_bad_lines=False'
    # to skip problematic rows
    dataset = pd.read_csv('/content/train.csv', engine='python', error_bad_lines=False)
    print("Warning: Skipped problematic rows due to parsing errors.")

# If encoding issues are suspected, try specifying the encoding:
# dataset = pd.read_csv('/content/train.csv', engine='python', encoding='latin-1') # or 'utf-8', 'iso-8859-1', etc.

# If the delimiter is not a comma, specify it using the 'sep' argument:
# dataset = pd.read_csv('/content/train.csv', engine='python', sep='\t') # for tab-separated values

# Inspect the data for inconsistencies:
print(dataset.head())  # View the first few rows to check for issues
print(dataset.tail())  # View the last few rows
print(dataset.isnull().sum())  # Check for missing values in each column

dataset.head()

dataset.shape

dataset.isnull().sum()

dataset['label'] = dataset['label'].replace({'fake':1,'real':0})

# separating the dataset
X = dataset['text']
Y = dataset['label']

Y

X

dataset.head()

"""Stemming:

Stemming is the process of reducing a word to its Root word

example: actor, actress, acting --> act
"""

port_stem = PorterStemmer()

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

dataset['text'] = dataset['text'].apply(stemming)

dataset['text']

#separating the data and label
X = dataset['text'].values
Y = dataset['label'].values

X

Y.shape

# converting the textual data to numerical data
vectorizer = TfidfVectorizer()
vectorizer.fit(X)

X = vectorizer.transform(X)

print(X)



"""Splitting the dataset to training & test data


"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, stratify=Y, random_state=2)

X_train.shape

"""Training the Model: Logistic Regression"""

model = LogisticRegression()

model.fit(X_train, Y_train)

"""Evaluation

accuracy score
"""

#accurancy score on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy score of training data : ', training_data_accuracy)

#accurancy score in test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('Accuracy score of test data : ', test_data_accuracy)

"""Making a Predictive System"""

x_test = X_test[2]

prediction = model.predict(x_test)
print(prediction)

if (prediction[0] == 0):
  print('The news is Real')
else:
  print('The news is Fake')

if Y_test[2] == 0:
  print('The news is Real')
else:
  print('The news is Fake')

