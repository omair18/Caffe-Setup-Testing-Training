import sys
sys.path.append("/home/omair/caffe-master/python")
import caffe
import numpy as np
import Image
import matplotlib
matplotlib.rcParams['backend'] = "Qt4Agg"
import numpy as np
import lmdb
caffe_root = '../'

MODEL_FILE = '/home/omair/caffe-master/Emotion6/deploy.prototxt'
PRETRAINED = '/home/omair/caffe-master/Emotion6/Emotion6_iter_90.caffemodel'
db_path = '/home/omair/caffe-master/Emotion6/emotion6_test'

#MODEL_FILE = '/home/omair/caffe-master/hybridCNN/hybridCNN_deploy.prototxt'
#PRETRAINED = '/home/omair/caffe-master/hybridCNN/hybridCNN_iter_700000.caffemodel'

net = caffe.Net(MODEL_FILE, PRETRAINED,caffe.TEST)
net1 = caffe.Classifier(MODEL_FILE, PRETRAINED,
                        raw_scale=255,
                        image_dims=(227,227))
caffe.set_mode_cpu()
lmdb_env = lmdb.open(db_path)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
count = 0
correct = 0
for key, value in lmdb_cursor:
    print "Count:"
    print count
    count = count + 1
    datum = caffe.proto.caffe_pb2.Datum()
    datum.ParseFromString(value)
    label = int(datum.label)
####
    image = caffe.io.datum_to_array(datum)
####
    image = image.transpose(1,2,0)
    image2 = image.astype(np.float32)
####
    print image2.shape, image2.dtype
    prediction = net1.predict([image2], oversample=False)
    print "Confidences:", prediction, "\nPredicted Label:", np.argmax(prediction), "\nTrue Label:", label 
    #sys.stdin.read(1)

 
''' 
    out = net.forward_all(data=np.asarray([image]))
    predicted_label = out['prob'][0].argmax(axis=0)
    print out['prob']
    if label == predicted_label[0][0]:
        correct = correct + 1
    print("Label is class " + str(label) + ", predicted class is " + str(predicted_label[0][0]))

    print(str(correct) + " out of " + str(count) + " were classified correctly")
''' 
