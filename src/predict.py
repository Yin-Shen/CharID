import numpy as np
import argparse
from keras.engine.topology import Layer
from keras.models import model_from_json
from keras import initializers
from keras import backend as K



import os 
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

parser = argparse.ArgumentParser(description='''add_feature''')
parser.add_argument("--dirs", "-d", required=True,
                    help="workspace dir")
args = parser.parse_args()


os.chdir(args.dirs+"/result")
data_test=np.load('data_predict.npy')
label_test=np.load('label_predict.npy')


class AttLayer(Layer):
    def __init__(self,**kwargs):
        # self.init = initializers.get('normal')
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
        # size of x :[batch_size, sel_len, attention_dim]
        # size of u :[batch_size, attention_dim]
        # uit = tanh(xW+b)
        uit = K.tanh(K.bias_add(K.dot(x, self.W), self.b))
        ait = K.dot(uit, self.u)
        ait = K.squeeze(ait, -1)

        ait = K.exp(ait)

        if mask is not None:
            # Cast the mask to floatX to avoid float64 upcasting in theano
            ait *= K.cast(mask, K.floatx())
        ait /= K.cast(K.sum(ait, axis=1, keepdims=True) + K.epsilon(), K.floatx())
        ait = K.expand_dims(ait)
        weighted_input = x * ait
        output = K.sum(weighted_input, axis=1)

        return output
    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])


model = model_from_json(open('model_architecture.json').read(), custom_objects = {'AttLayer': AttLayer})
model.load_weights('model_weights.h5')

pred=model.predict(data_test)

o=open('predict_whole.txt','w')
for i in pred.tolist():
    if float(list(i)[0]) >= 0.5:
       o.write(str('1')+'\n')
    else:
       o.write(str('0') + '\n')
o.close()
