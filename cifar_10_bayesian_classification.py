# -*- coding: utf-8 -*-
"""CIFAR_10_Bayesian_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/119QveEFsbU7iouz6s1vm-PY4S40NcLMt

Design a Bayesian Classifier using PCA features for the same 10-class data set 
( Use the data to compute PCA features, estimate the distributions (either parametric or using Parzen’s technique))
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras import datasets
from sklearn.neighbors import KernelDensity

"""Load and preprocess the dataset """

(x_train, y_train), (x_test, y_test) = datasets.cifar10.load_data()

# Flatten the images and convert labels to 1D arrays
x_train = x_train.reshape(x_train.shape[0], -1)
x_test = x_test.reshape(x_test.shape[0], -1)
y_train = y_train.ravel()
y_test = y_test.ravel()

# Standardize the data
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

"""Perform PCA on the dataset """

# Choose the number of PCA components
n_components = 100

pca = PCA(n_components=n_components)
x_train_pca = pca.fit_transform(x_train)
x_test_pca = pca.transform(x_test)

"""Estimate the distributions using Parzen's technique:

"""

# Choose the kernel bandwidth
bandwidth = 0.1

# Train Kernel Density Estimation (KDE) models for each class
kde_models = []
for i in range(10):
    kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth)
    kde.fit(x_train_pca[y_train == i])
    kde_models.append(kde)

"""Classify test samples using the trained KDE models:

"""

# gnb = GaussianNB()
# gnb.fit(x_train_pca, y_train)
# Calculate the log probability of each test sample belonging to each class
log_probs = np.zeros((x_test_pca.shape[0], 10))
for i, kde in enumerate(kde_models):
    log_probs[:, i] = kde.score_samples(x_test_pca)

# Predict the class with the highest log probability
y_pred = np.argmax(log_probs, axis=1)

# y_pred = gnb.predict(x_test_pca)
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)

# # Classification report
# print(classification_report(y_test, y_pred))

# Evaluate the classifier:
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Classification report
print(classification_report(y_test, y_pred))