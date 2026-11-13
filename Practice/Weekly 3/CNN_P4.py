import keras
from keras import layers
import warnings

warnings.filterwarnings('ignore')

(xtrain,ytrain),(xtest,ytest) = keras.datasets.mnist.load_data()

xtrain = xtrain/255.0
xtest = xtest/255.0

# xtrain = xtrain[:1000]
# xtest = xtest[:1000]
# ytrain = ytrain[:1000]
# ytest = ytest[:1000]

model = keras.Sequential([
    layers.Input((28,28,1)),

    layers.Conv2D(32,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Flatten(),

    layers.Dense(64, activation='relu'),
    layers.Dense(128, activation='relu'),

    layers.Dense(10,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(xtrain,ytrain,batch_size=50,epochs=5)

test_loss, test_accuracy = model.evaluate(xtest,ytest)

print(test_accuracy)