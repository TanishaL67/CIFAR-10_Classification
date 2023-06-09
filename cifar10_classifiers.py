**Analysis and comparison of Statistical methods versus Neural Networks. 
**

OBJECTIVE:

The main objective of the project is to analyze and compare different statistical methods and neural networks for image classification.
We will explore three different algorithms to classify the images of the CIFAR-10 dataset. 
We considered the following classifiers:
1. Bayesian Classifiers with PCA for feature selection 
2. K-Nearest Neighbors (KNN)
3. Convolutional Neural Networks (CNN)
for the image classification. 

Our objective is to explore these techniques and identify the technique that can achieve the highest possible classification accuracy. 

CIFAR-10 dataset consists of 60,000 different images accross 10 different classes. The classes include airplane, automobile, bird, cat, deer, dog, frog, horse, ship, and truck. 

Let us start our analyses and try the different algorithm to sucessfully reach the goal.


We started with importing all the required libraries:
Tensorflow, mainly used to load the dataset, create and train neural networks.
Numpy will be used to handle large arrays and matrices.
Sklearn to be able to use functions like PCA and split the data into trian and test datasets and create the bayes theorm based classifiers.

#importing the tensorflow library 
import tensorflow as tf

# Display the version
print(tf.__version__)	

# other imports
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KernelDensity


Next we loaded the dataset using tenosrflow and spliting the dataset into test and train sets.

# Loading the dataset available on the tensorflow keras API)
data1 = tf.keras.datasets.cifar10

# dividing the dataset into train and test sets using the load_data() function.
(X_train,Y_train),(X_test,Y_test) = data1.load_data()

#print the shapes and sizes of the test and train sets 
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

#we found the shapes to be:
#(50000, 32, 32, 3) (50000, 1) (10000, 32, 32, 3) (10000, 1)

We then proceeded to preprocess the CIFAR 10 dataset It consists of 60000 images across 10 different classes. Now we precprocessed the dataset using reshape command to flatten each image and normalizing the pixel values to the range [0 1].

# Reduce pixel values
X_train, X_test = X_train / 255.0, X_test / 255.0

# Flatten the images and convert labels values to 1D arrays
Y_train, Y_test = Y_train.flatten(), Y_test.flatten()


Now to explore the pictures in the dataset we will create a subplot in a 5*5 grid from the x_train dataset.

# visualize data by plotting images
fig, ax = plt.subplots(5, 5)
k = 0
 
for i in range(5):
    for j in range(5):
        ax[i][j].imshow(X_train[k], aspect='auto')
        k += 1
 
 
plt.show()

Now we flatten the X_train dataset too.

#Flatten the class label
x_train = X_train.reshape(X_train.shape[0], -1)
x_test = X_test.reshape(X_test.shape[0], -1)

# Bayesian Classifier

The first classification algorithm we used is Byaesian Classifier. It is a machinelearning model that uses Bayes theorm to classify imput samples into one of the classes. When given the input vector of all the feature values, it calculates the probability of each class and then the input image is assigned to the class with the highest posterior probability 

In the below code we will use Principal Component Analysis to handle the high dimentionality of the raw image data, by reducing the number of features while preserving most of the variance in the data. Once the dimentionality of the input vectore is reduced, the classifier can estimate the class conditional probability and prior probability to compute the posterior probabilities for each class. 

We standardise the input data i.e. we will scale the features such that they have variance as 1 and mean as 0.

# Standardize the data
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

Now we will use PCA for dimensionality reduction 

# Choose the number of PCA components
#first we tried it for 30 components that gave us an accuracy of 21 percent by increasing the number of components to 50 
#it increased to 22.04 and at 60 it finally came out to be 23.14 which was the highest for the bayesian classifier.
n_components = 60

pca = PCA(n_components=n_components)
x_train_pca = pca.fit_transform(x_train)
x_test_pca = pca.transform(x_test)

Estimate the distributions using Parzen's technique:

# Choose the kernel bandwidth
bandwidth = 0.1

# Train Kernel Density Estimation (KDE) models for each class
kde_models = []
for i in range(10):
    kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth)
    kde.fit(x_train_pca[Y_train == i])
    kde_models.append(kde)

Classify test samples using the trained KDE models:


# Calculate the log probability of each test sample belonging to each class
log_probs = np.zeros((x_test_pca.shape[0], 10))
for i, kde in enumerate(kde_models):
    log_probs[:, i] = kde.score_samples(x_test_pca)

# Predict the class with the highest log probability
y_pred1 = np.argmax(log_probs, axis=1)

We now evaluated the classifier and printied the classification report

# Evaluate the classifier:
accuracy = accuracy_score(Y_test, y_pred1)
print("Accuracy:", accuracy)

# Classification report
print(classification_report(Y_test, y_pred1))

# generate the confusion matrix
cm = confusion_matrix(Y_test, y_pred1)

# print('Confusion matrix\n\n', cm)

print('\nTrue Positives(TP) = ', cm[0,0])

print('\nTrue Negatives(TN) = ', cm[1,1])

print('\nFalse Positives(FP) = ', cm[0,1])

print('\nFalse Negatives(FN) = ', cm[1,0])

# Define the labels for the heatmap
labels = ['True Negatives', 'False Positives', 'False Negatives', 'True Positives']

# Define the values for the heatmap
tp = cm[0][0]
tn = cm[1][1]
fp = cm[0][1]
fn = cm[1][0]

# Define the color scheme for the heatmap
cmap = plt.cm.Blues

# Create the heatmap using the values and labels
plt.imshow([[tn, fp], [fn, tp]], interpolation='nearest', cmap=cmap)
plt.xticks(np.arange(2), ['Negative', 'Positive'])
plt.yticks(np.arange(2), ['Negative', 'Positive'])
plt.colorbar()

# Add the labels to the heatmap
for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i][j]), ha='center', va='center', color='black', fontsize=14)
plt.title('Heatmap for Bayes')
plt.show()

# Gaussian Naive Bayes (GNB) classifier

We can also try to create and fit a gaussian Naive Bias. Similar to the Above bayesian classifier it uses the Bayes theorm, the only difference is that it assumes that the features are conditionally independent. 

# initialize a Gaussian Naive Bayes classifier.
gnb = GaussianNB()

# fit the Gaussian Naive Bayes classifier using the PCA-transformed training data
gnb.fit(x_train_pca, Y_train)

Now we will evaluate this model too:

y_pred = gnb.predict(x_test_pca)
accuracy = accuracy_score(Y_test, y_pred)
print("Accuracy:", accuracy)

# Classification report
print(classification_report(Y_test, y_pred))

# generate the confusion matrix
cm = confusion_matrix(Y_test, y_pred_gnb)

# print('Confusion matrix\n\n', cm)

print('\nTrue Positives(TP) = ', cm[0,0])

print('\nTrue Negatives(TN) = ', cm[1,1])

print('\nFalse Positives(FP) = ', cm[0,1])

print('\nFalse Negatives(FN) = ', cm[1,0])

# Define the labels for the heatmap
labels = ['True Negatives', 'False Positives', 'False Negatives', 'True Positives']

# Define the values for the heatmap
tp = cm[0][0]
tn = cm[1][1]
fp = cm[0][1]
fn = cm[1][0]

# Define the color scheme for the heatmap
cmap = plt.cm.Blues

# Create the heatmap using the values and labels
plt.imshow([[tn, fp], [fn, tp]], interpolation='nearest', cmap=cmap)
plt.xticks(np.arange(2), ['Negative', 'Positive'])
plt.yticks(np.arange(2), ['Negative', 'Positive'])
plt.colorbar()

# Add the labels to the heatmap
for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i][j]), ha='center', va='center', color='black', fontsize=14)
plt.title('Heatmap for GNB')
plt.show()

We saw that the accuarcy increases to 35.45% when instead of Parzen's method we used Naive Bias Classifier.

# K-Nearest Neighbors (KNN)

K-Nearest Neighbors (KNN) classifier is a supervised machine learning algorithm. It works by finding the k-nearest neighbors of the given data point in the feature space and assigning it a class label based on the majority class label among these neighbors.

# Choose the number of neighbors (k)
# k = 10#0.351
k = 5 
#0.3567
# k= 15 #0.3507
#k=20

# Create a K-Nearest Neighbor classifier
knn = KNeighborsClassifier(n_neighbors=k, weights='distance', n_jobs=-1, metric='minkowski', p=1)
knn.fit(x_train, Y_train)


Now evaluating the performance of the KNN 

#Evaluate the classifier
y_pred2 = knn.predict(x_test)
accuracy = accuracy_score(Y_test, y_pred2)
print("Accuracy for KNN:", accuracy)

#Classification report
print("Classification Report for KNN: \n", classification_report(Y_test, y_pred2))

To improve the classification accuracy of the model we will try using the train test that has been passed thorugh PCA.

#to increase the classification accuracy we will fit the data with that was passed through principal component analysis.
knn.fit(x_train_pca, Y_train)

# Evaluate the classifier
y_pred_knn1 = knn.predict(x_test_pca)
accuracy_knn = accuracy_score(Y_test, y_pred_knn1)
print("Accuracy for KNN:", accuracy_knn)

# Classification report
print("Classification Report for KNN:\n", classification_report(Y_test, y_pred_knn1))

# generate the confusion matrix
cm = confusion_matrix(Y_test, y_pred_knn)

# print('Confusion matrix\n\n', cm)

print('\nTrue Positives(TP) = ', cm[0,0])

print('\nTrue Negatives(TN) = ', cm[1,1])

print('\nFalse Positives(FP) = ', cm[0,1])

print('\nFalse Negatives(FN) = ', cm[1,0])

# Define the labels for the heatmap
labels = ['True Negatives', 'False Positives', 'False Negatives', 'True Positives']

# Define the values for the heatmap
tp = cm[0][0]
tn = cm[1][1]
fp = cm[0][1]
fn = cm[1][0]

# Define the color scheme for the heatmap
cmap = plt.cm.Blues

# Create the heatmap using the values and labels
plt.imshow([[tn, fp], [fn, tp]], interpolation='nearest', cmap=cmap)
plt.xticks(np.arange(2), ['Negative', 'Positive'])
plt.yticks(np.arange(2), ['Negative', 'Positive'])
plt.colorbar()

# Add the labels to the heatmap
for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i][j]), ha='center', va='center', color='black', fontsize=14)
plt.title('Heatmap for KNN')
plt.show()

# Convolutional Neural Networks (CNNs)
Next approach we tried is the Convolutional Neural Network (CNN). It is highly effective for image classification tasks. We have already preprocessed the data now we design a CNN architecture, which consists of multiple convolutional layers, pooling layers and fully connected layers as well as dropout and normalization layers.

# number of classes
K = len(set(Y_train))
 
# calculate total number of classes
# for output layer
print("number of classes:", K)
 
# Build the model using the functional API
# input layer
i = Input(shape=X_train[0].shape)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(i)
x = BatchNormalization()(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)
 
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)

x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2, 2))(x)
 
x = Flatten()(x)
x = Dropout(0.2)(x)
 
# Hidden layer
x = Dense(1024, activation='relu')(x)
x = Dropout(0.2)(x)
 
# last hidden layer i.e.. output layer
x = Dense(K, activation='softmax')(x)
 
model = Model(i, x)
 


To know more about the model we print the model summary.

# model description
model.summary()

Now we will compile the model with the specified optimizer, loss function, and metric, so that we can move forward to fit the model.

# Compile the model
model.compile(optimizer='adam',
			loss='sparse_categorical_crossentropy',
			metrics=['accuracy'])

Now we train the model on the provided training data while also evaluating it on the validation data. During each epoch, the model updates its weights to minimize the loss function. 

# Fitting the model on the train dataset
r = model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=50)


We will perform data augmentation and train the CNN model with the augmented data using model.fit(). 

# Fit with data augmentation
# Note: if you run this AFTER calling
# the previous model.fit()
# it will CONTINUE training where it left off
batch_size = 32
data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)

train_generator = data_generator.flow(X_train, Y_train, batch_size)
steps_per_epoch = X_train.shape[0] // batch_size

r = model.fit(train_generator, validation_data=(X_test, Y_test),
			steps_per_epoch=steps_per_epoch, epochs=50)


We will plot the training and vailidation accuracy at each epoch during the model trainig process, with the training accuracy in red and the validation accuracy in green.

# Plot accuracy per iteration
plt.plot(r.history['accuracy'], label='acc', color='red')
plt.plot(r.history['val_accuracy'], label='val_acc', color='green')
plt.legend()

We calculate the average training and validation accuracies, evaluate the model on the test set, and print the results.
This will help us understand the performances of the trained models and the final test accuracy after evaluating the model on the test set.

# Calculate average accuracies
average_train_accuracy = np.mean(r.history['accuracy'])
average_val_accuracy = np.mean(r.history['val_accuracy'])

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print(f"Average Training Accuracy: {average_train_accuracy * 100:.2f}%")
print(f"Average Validation Accuracy: {average_val_accuracy * 100:.2f}%")
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

Let us now print the confusion matrix for this too.
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Generate the confusion matrix
confusion_mtx = confusion_matrix(Y_test, y_pred_classes)

# Plot the confusion matrix as a heatmap
plt.figure(figsize=(10,8))
sns.heatmap(confusion_mtx, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

To show the use of the trained model to make predictions on individual images from the test dataset and compare the results to the ground truth labels we will predict the class label of a single image from the CIFAR-10 test dataset and compare it to the original label.

# label mapping

labels = '''airplane automobile bird cat deerdog frog horseship truck'''.split()

# select the image from our test dataset
image_number = 0

# display the image
plt.imshow(X_test[image_number])

# load the image in an array
n = np.array(X_test[image_number])

# reshape it
p = n.reshape(1, 32, 32, 3)

# pass in the network for prediction and
# save the predicted label
predicted_label = labels[model.predict(p).argmax()]

# load the original label
original_label = labels[Y_test[image_number]]

# display the result
print("Original label is {} and predicted label is {}".format(
	original_label, predicted_label))


# save the model
model.save('CIFAR10.Classification.h5')

We will compare the details of different models in the report.
