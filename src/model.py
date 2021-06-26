'''
This script is training cnn model for charid-anchor.

Author: Yin Shen
'''
import sys
import argparse
import time
import numpy as np
from keras.layers import Input,Bidirectional,GRU
from keras.models import Model
from keras.callbacks import ModelCheckpoint,EarlyStopping 
from keras.layers.core import Dense, Dropout
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.engine.topology import Layer
from keras.optimizers import Adagrad
from sklearn.metrics import roc_curve, auc
from keras import initializers
from keras import backend as K
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#specify which GPU(s) to be used
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"



parser = argparse.ArgumentParser(description="Training Charid-anchor cnn model")
parser.add_argument("--epochs", "-e", default=150, type=int, required=False,
                    help="Number of epochs.(default is 150)")
parser.add_argument("--patience", "-p", default=20, type=int, required=False,
                    help='Number of epochs  for early stopping.(default is 20)')
parser.add_argument("--learningrate", "-lr", default=0.001, type=float, required=False,
                   help='Learning rate.(default is 0.01)')
parser.add_argument("--batch_size","-b",  default=128, type=int, required=False,	
                    help="Batch Size.(default is 128)")
parser.add_argument("--dropout","-r",  default=0.7, required=False,
                    help="Dropout rate.(default is 0.7)")
parser.add_argument("--nb_filter1","-n1",  default=200, type=int, required=False,
                    help="Number of filters in first layer of convolution.(default is 200)")
parser.add_argument("--nb_filter2","-n2",  default=100, type=int, required=False,
                    help="Number of filters in second layer of convolution.(default is 100)")
parser.add_argument("--nb_filter3","-n3",  default=100, type=int, required=False,
                    help="Number of filters in third layer of convolution.(default is 100)")
parser.add_argument("--nb_filter4","-n4",  default=64, type=int, required=False,
                    help="Number of filters in fourth layer of convolution.(default is 64)")
parser.add_argument("--filter_len1","-fl1",  default=19, type=int, required=False,
                    help="length of filters in first layer of convolution.(default is 19)")
parser.add_argument("--filter_len2","-fl2",  default=11, type=int, required=False,
                   help="length of filters in second layer of convolution.(default is 11)")
parser.add_argument("--filter_len3","-fl3",  default=11, type=int, required=False,
                    help="length of filters in third layer of convolution.(default is 11)")
parser.add_argument("--filter_len4","-fl4",  default=7, type=int, required=False,
                    help="length of filters in fourth layer of convolution.(default is 7)")
parser.add_argument("--pooling_size1","-ps1",  default=5, type=int, required=False,
                    help="length of max_pooling size in first layer of convolution.(default is 5)")
parser.add_argument("--pooling_size2","-ps2",  default=5, type=int, required=False, 
                    help="length of max_pooling size in second layer of convolution.(default is 5)")
parser.add_argument("--pooling_size3","-ps3",  default=5, type=int, required=False, 
                    help="length of max_pooling size in third layer of convolution.(default is 5)")
parser.add_argument("--pooling_size4","-ps4",  default=2, type=int, required=False,
                    help="length of max_pooling size in fourth layer of convolution.(default is 2)")
parser.add_argument("--GRU","-gru",  default=80, type=int, required=False,
                    help="units in the gru layer.(default is 80)")
parser.add_argument("--hidden","-hd", default=200, type=int, required=False,
                    help="units in the fully connected layer.(default is 200)")
args = parser.parse_args()

class AttLayer(Layer):
    def __init__(self,**kwargs):
        self.init = initializers.RandomNormal(seed=10)
        self.supports_masking = True
        self.attention_dim = 80
        super(AttLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        assert len(input_shape) == 3
        self.W = K.variable(self.init((input_shape[-1], self.attention_dim)))
        self.b = K.variable(self.init((self.attention_dim, )))
        self.u = K.variable(self.init((self.attention_dim, 1)))
        self.trainable_weights = [self.W, self.b, self.u]
        super(AttLayer, self).build(input_shape)

    def compute_mask(self, inputs, mask=None):
        return mask

    def call(self, x, mask=None):
        uit = K.tanh(K.bias_add(K.dot(x, self.W), self.b))
        ait = K.dot(uit, self.u)
        ait = K.squeeze(ait, -1)
        ait = K.exp(ait)
        if mask is not None:
            ait *= K.cast(mask, K.floatx())
        ait /= K.cast(K.sum(ait, axis=1, keepdims=True) + K.epsilon(), K.floatx())
        ait = K.expand_dims(ait)
        weighted_input = x * ait
        output = K.sum(weighted_input, axis=1)
        return output

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])

sys.stdout.flush()

data_train=np.load('data_train.npy')
label_train=np.load('label_train.npy')
data_val=np.load('data_val.npy')
label_val=np.load('label_val.npy')
data_test=np.load('data_test.npy')
label_test=np.load('label_test.npy')

np.random.seed(666)

sequence_input = Input(shape=(1000,4))
x = Conv1D(int(args.nb_filter1),
           int(args.filter_len1),
           border_mode='same',activation='relu')(sequence_input)
x = MaxPooling1D(int(args.pooling_size1))(x)

x = Conv1D(int(args.nb_filter2),
           int(args.filter_len2),
           border_mode='same',activation='relu')(x)
x = MaxPooling1D(int(args.pooling_size2))(x)

x = Conv1D(int(args.nb_filter3), 
           int(args.filter_len3),
           border_mode='same',activation='relu')(x)
x = MaxPooling1D(int(args.pooling_size3))(x)

x = Conv1D(int(args.nb_filter4),
           int(args.filter_len4),
           border_mode='same',activation='relu')(x)
x = MaxPooling1D(int(args.pooling_size4))(x)

x = Bidirectional(GRU(int(args.GRU), return_sequences = True), merge_mode = 'concat')(x)

x = AttLayer()(x)

x = Dropout(float(args.dropout))(x)

x = Dense(int(args.hidden),init='normal', activation='relu')(x)
x = Dropout(float(args.dropout))(x)

preds = Dense(1,init='normal', activation='sigmoid')(x)
model = Model(sequence_input, preds)
print(model.summary())

adagrad_new = Adagrad(lr=float(args.learningrate))
print('model compiling...')
sys.stdout.flush()
model.compile(loss='binary_crossentropy',optimizer=adagrad_new,metrics=['accuracy'])  
early_stopping =EarlyStopping(monitor='val_loss', patience=args.patience,verbose=1)
checkpointer = ModelCheckpoint(filepath='model_weights.h5', verbose=1, save_best_only=True)


print('training...')

time_start = time.time()
result=model.fit(data_train,label_train,batch_size=args.batch_size,nb_epoch=args.epochs,shuffle=True,validation_data=(data_val,label_val),callbacks=[checkpointer, early_stopping])
time_end = time.time()

json_string=model.to_json()
open('model_architecture.json','w').write(json_string)

model.load_weights('model_weights.h5')
score = model.evaluate(data_val,label_val, verbose=0)
print('accuracy_validate :',score[1])

score1 = model.evaluate(data_test,label_test, verbose=0)
print('Test loss:', score1[0])
print('Test accuracy:', score1[1])


print('training time : %d sec' % (time_end-time_start))

print('plot ROC curve...')

pred=model.predict(data_test)

fpr, tpr, thresholds = roc_curve(label_test, pred)
roc_auc = auc(fpr, tpr)
print('the auc is ',roc_auc)


plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig('pictureROC.png')
plt.close()

plt.plot(result.history['loss'])
plt.plot(result.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('pictureloss.png')
plt.close()


print('plot figure...')

plt.figure
plt.plot(result.epoch,result.history['acc'],label="acc")
plt.plot(result.epoch,result.history['val_acc'],label="val_acc")
plt.scatter(result.epoch,result.history['acc'],marker='*')
plt.scatter(result.epoch,result.history['val_acc'])
plt.legend(loc='best')
plt.savefig('picturehistory.png')
plt.close()

