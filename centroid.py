import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from matplotlib import pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images[:10000,:,:]
train_labels = train_labels[:10000]
test_images = test_images[:1000,:,:]
test_labels  = test_labels[:1000]
print(
    "Training Data Shape is {} ,  Its Type Is {} ,\nTest Data Shape is {} , Its Type is {} ".format(
        train_images.shape , type(train_images) , test_images.shape , type(test_images)
    )
)

def imaged_grid(img , row , col ):
    """
        return same input but divided in nGrid Images  
        each image with dimensions row * col
    """
    x , y = img.shape

    assert x % row == 0
    assert y % col == 0
    
    return (img.reshape ( x //row, row, -1, col)
               .swapaxes(1,2)
               .reshape(-1, row, col))

print(imaged_grid(test_images[2] , 4, 4 ).shape)
imaged_grid(test_images[2] , 4 , 4 )

def get_centroid(img):
    
    feature_vector = []
 
    for grid in imaged_grid(img , 4 , 4 ) :
        
        Xc = 0 
        Yc = 0 
        sum = 0
    
        for index, x in np.ndenumerate(grid):
          sum+= x 
          Xc += x * index[0]
          Yc += x * index[1]
        
        if sum != 0 :
            feature_vector.append( Xc/ sum )
            feature_vector.append(Yc/ sum )
        else :
             feature_vector.append(0)
             feature_vector.append(0)
        
    
    return np.array(feature_vector)

print("Feature Extraction From Training Data")
train_features = [get_centroid(img)  for img in train_images  ]
print("Extraction is Done")

train_features = np.array(train_features)
train_features.shape

print("Feature Extraction From Test Data")
test_features = [get_centroid(img)  for img in test_images  ]
print("Extraction is Done")

test_features = np.array(test_features)
test_features.shape

def KNN(train_features, test_features, train_labels):
    knn = KNeighborsClassifier(1)
    knn.fit(train_features, train_labels)  
    prediction = knn.predict(test_features)  
    return prediction

Knn_prediction = KNN(train_features, test_features , train_labels )
print("Accuracy Score =", accuracy_score(test_labels, Knn_prediction) * 100, "%")
