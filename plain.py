#Basic CNN Implementation of CIFAR-10

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dropout, Activation, Conv2D, AveragePooling2D,GlobalAveragePooling2D, MaxPooling2D,merge,ZeroPadding2D,Flatten,Dense
from keras.utils import np_utils
from keras.optimizers import Adadelta
from keras.models import Model
from keras.layers.core import Lambda
from keras.callbacks import ModelCheckpoint
from keras.callbacks import LearningRateScheduler
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
import pandas
import cPickle
import math
import numpy as np
from keras.constraints import maxnorm


batch_size = 32
nb_classes = 10
nb_epoch = 30
acc=[]
loss=[]
val_acc=[]
val_loss=[]


#unpickle is load the cifar 10 data stored in pickled files

def unpickle(file):
    
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo)
    return dict

rows, cols = 32, 32
channels = 3

#datapower 256 contains data which has 256 colours without quantization
x = unpickle('datapower256')
X_train=x['data'][:40000]
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
xx=unpickle('datalabels')
Y_train=xx['labels'][:40000]
"""
#test batch
test=unpickle('testbatch')
X_test=test['data']
Y_test=test['labels']
print('X_test shape:', X_test.shape)
print(X_test.shape[0], 'test samples')
"""
#validation batch
valid=unpickle('validation_batch')
X_valid=valid['data']
Y_valid=valid['labels']
print('X_validation shape:', X_valid.shape)
print(X_valid.shape[0], 'validation samples')
print(Y_train.shape[0],'Y train shape')



Y_train = np_utils.to_categorical(Y_train, 10)

Y_valid = np_utils.to_categorical(Y_valid, 10)


def create_model():
    model = Sequential()

    model.add(Conv2D(32,(3,3),padding='same',input_shape=(32,32,3)))
    model.add(Activation('relu'))
    
    model.add(Conv2D(32,(3,3)))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.5))

    model.add(Conv2D(64,(3,3),padding='same'))
    model.add(Activation('relu'))
    
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))


    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.5))

    model.add(Conv2D(128,(3,3),padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(128,(3,3)))
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))

    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.summary()
    

    

    
    return model


X_train = X_train.astype('float32')
#X_test = X_test.astype('float32')
X_valid = X_valid.astype('float32')
X_train /= 255
#X_test /= 255
X_valid/=255


# Global Contrast Normalization
mean = np.mean(X_train, axis=0).astype(np.float32)
mean = np.mean(X_valid, axis=0).astype(np.float32)
std = np.mean(X_train, axis=0).astype(np.float32)
std = np.mean(X_valid, axis=0).astype(np.float32)

X_train = X_train.astype(np.float32) - mean
X_train/=std
X_valid = X_valid.astype(np.float32) - mean
X_valid/=std




i=8
if(i==2):
    c_model=create_model()
    ada=Adadelta()
    c_model.compile(loss='categorical_crossentropy', optimizer=ada, metrics=['accuracy'])
    # Fit the model on the batches generated by datagen.flow().
    j=int(pow(2,i))
    filepath="WEIGHT"+str(j)+".hdf5"
    checkpoint=ModelCheckpoint(filepath,monitor='val_acc',verbose=1,save_best_only=True,save_weights_only=True,mode='max')
    callback=[checkpoint]
     
    """
    datagen = ImageDataGenerator(
    zca_whitening=True,
    
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

    datagen.fit(X_train)

    # fits the model on batches with real-time data augmentation:
    history_callback=c_model.fit_generator(datagen.flow(X_train, Y_train, batch_size=32),
                    steps_per_epoch=X_train.shape[0], epochs=nb_epoch,validation_data=(X_valid, Y_valid), callbacks=callback,verbose=1)


    """
    history_callback=c_model.fit(X_train, Y_train,
                                     batch_size=batch_size,
                    
                        epochs=nb_epoch, validation_data=(X_valid, Y_valid), callbacks=callback,verbose=1)

    loss = history_callback.history['loss']
    val_loss = history_callback.history['val_loss']
    acc=history_callback.history['acc']
    val_acc=history_callback.history['val_acc']
    with open("OUT_loss"+str(j)+".txt", "w") as f:
    	for s in loss:
        	f.write(str(s) +"\n")
    f.close()
   
    with open("OUT_vloss"+str(j)+".txt", "w") as f:
    	for s in val_loss:
    	    f.write(str(s) +"\n")
    f.close()

    with open("OUT_acc"+str(j)+".txt", "w") as f:
    	for s in acc:
    	    f.write(str(s) +"\n")
    f.close()

    with open("OUT_vacc"+str(j)+".txt", "w") as f:
    	for s in val_acc:
    	    f.write(str(s) +"\n")
    f.close()


    

    
   

else:
    c_model=create_model()
    m=int(pow(2,i-1))
    c_model.load_weights("WEIGHT"+str(m)+".hdf5")
    ada=Adadelta()
    c_model.compile(loss='categorical_crossentropy', optimizer=ada, metrics=['accuracy'])
    # Fit the model on the batches generated by datagen.flow().
    j=int(pow(2,i))
    filepath="WEIGHT"+str(j)+".hdf5"
    checkpoint=ModelCheckpoint(filepath,monitor='val_acc',verbose=1,save_best_only=True,save_weights_only=True,mode='max')
    callback=[checkpoint]

    """
    datagen = ImageDataGenerator(
    zca_whitening=True,
 
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

    datagen.fit(X_train)

    # fits the model on batches with real-time data augmentation:
    history_callback=c_model.fit_generator(datagen.flow(X_train, Y_train, batch_size=32),
                    steps_per_epoch=X_train.shape[0], epochs=nb_epoch,validation_data=(X_valid, Y_valid), callbacks=callback,verbose=1)


   
    


    """
    history_callback=c_model.fit(X_train, Y_train,
                                     batch_size=batch_size,
                    
                        epochs=nb_epoch, validation_data=(X_valid, Y_valid), callbacks=callback,verbose=1)
    
    loss=(history_callback.history['loss'])
    val_loss = history_callback.history['val_loss']
    acc=history_callback.history['acc']
    val_acc=history_callback.history['val_acc']

    with open("OUT_loss"+str(j)+".txt", "w") as f:
    	for s in loss:
        	f.write(str(s) +"\n")
    f.close()
   
    with open("OUT_vloss"+str(j)+".txt", "w") as f:
    	for s in val_loss:
    	    f.write(str(s) +"\n")
    f.close()

    with open("OUT_acc"+str(j)+".txt", "w") as f:
    	for s in acc:
    	    f.write(str(s) +"\n")
    f.close()


    with open("OUT_vacc"+str(j)+".txt", "w") as f:
    	for s in val_acc:
    	    f.write(str(s) +"\n")
    f.close()


   
"""

if (i==7):
    
    x=[]
    x=list(xrange(0,175))

    plt.subplot(211)  
    
    plt.plot(x,acc)  
    plt.plot(x,val_acc)  
    plt.title('model accuracy')  
    plt.ylabel('accuracy')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'test'], loc='upper left')  

    plt.subplot(212)  
    plt.plot(x,loss)  
    plt.plot(x,val_loss)  
    plt.title('model loss')  
    plt.ylabel('loss')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'test'], loc='upper left')  
    plt.savefig("PLOT.png")

"""
   

    
    
