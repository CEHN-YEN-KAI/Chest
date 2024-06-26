# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 16:08:12 2021

@author: EN308
"""

import warnings 
warnings.filterwarnings('ignore',category=FutureWarning) #because of numpy version
import tensorflow as tf
from tensorflow.keras import backend as K
K.clear_session()

import os
from tensorflow.keras.initializers import he_normal
from tensorflow.keras import applications, activations
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, SeparableConv2D, BatchNormalization, ZeroPadding2D, GlobalAveragePooling2D,Flatten,Average, Dropout
from tensorflow.keras.layers import Add, Activation, Dropout, Flatten, Dense, Lambda, LeakyReLU, PReLU
from tensorflow.keras.applications import VGG16
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import cv2
import numpy as np
import itertools
import glob
import struct
import zlib

import pickle
import shutil
import statistics
from math import pi
from math import cos
from math import floor
from tensorflow.keras import backend
import statistics
from scipy import interp
from skimage.segmentation import mark_boundaries
from sklearn.metrics import precision_recall_curve, average_precision_score, matthews_corrcoef, mean_squared_error, mean_squared_log_error
from sklearn.metrics import classification_report,confusion_matrix, roc_curve, auc, accuracy_score, log_loss
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, ReduceLROnPlateau, EarlyStopping, CSVLogger

from itertools import cycle
from sklearn.utils import class_weight
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam, SGD
from sklearn.preprocessing import label_binarize
from scipy.ndimage.interpolation import zoom
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn import metrics
from scipy.optimize import minimize
import time
import pandas as pd
from sklearn.metrics import confusion_matrix
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.optimizers import Adam, SGD
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
import numpy as np
import tensorflow as tf
from itertools import cycle
from sklearn.utils import class_weight

from sklearn.model_selection import train_test_split
from PIL import Image
import imageio
from glob import glob
import skimage.io as io
from tensorflow.keras.metrics import mean_absolute_error

def resnet_bs(num_filters=64, num_res_blocks=16, res_block_scaling=None):
    x_in = Input(shape=(512,512,1))
    x = b = Conv2D(num_filters, (3, 3), padding='same')(x_in)
    for i in range(num_res_blocks):
        b = res_block(b, num_filters, res_block_scaling)
    b = Conv2D(num_filters, (3, 3), padding='same')(b)
    x = Add()([x, b])
    x = Conv2D(1, (3, 3), padding='same')(x)
    return Model(x_in, x, name="ResNet-BS")

def res_block(x_in, filters, scaling):
    x = Conv2D(filters, (3, 3), padding='same', activation='relu')(x_in)
    x = Conv2D(filters, (3, 3), padding='same')(x)
    if scaling:
        x = Lambda(lambda t: t * scaling)(x)
    x = Add()([x_in, x])
    return x

resnet_bs = resnet_bs(num_filters=64, num_res_blocks=22, res_block_scaling=0.1)
resnet_bs.summary()

#load model:
resnet_bs.load_weights("./saved_models/ResNet-BS.bestjsrt4500_num_filters_64_num_res_blocks_22.h5") 
print("Loaded model from disk")
resnet_bs.summary()

source = glob(r'./result/image_or_size/*.png')
source.sort()

for f in source:
    img = Image.open(f).convert('L')
    img_name = f.split(os.sep)[-1]
    
    #preprocess the image
    x = image.img_to_array(img)
    x = x.astype('float32') / 255
    x1 = np.expand_dims(x, axis=0)
    
    #predict on the image
    pred = resnet_bs.predict(x1)
    test_img = np.reshape(pred, (512,512,1)) 
    imageio.imwrite("./result/image_or_size_bs/{}.png".format(img_name[:-4]), test_img)
    
    read_mask = cv2.imread("./result/lung_mask/{}.png".format(img_name[:-4]),0)
    read_image = cv2.imread("./result/image_or_size_bs/{}.png".format(img_name[:-4]),0)       
    bs_image=cv2.add(read_image, np.zeros(np.shape(read_image), dtype=np.uint8), mask=read_mask)
    #肺部分割影像
    imageio.imwrite("./result/mask_image_area_bs/{}.png".format(img_name[:-4]), bs_image)
		