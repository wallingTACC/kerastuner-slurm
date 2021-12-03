#!/usr/bin/env python

import xarray as xr
import numpy as np
import pandas as pd
#from tensorflow import keras
import tensorflow as tf
import kerastuner as kt
#from keras.models import Sequential
#from keras.layers import Dense
#from tf.keras.optimizers import SGD
#import matplotlib.pyplot as plt
import os
import h5py
import sys

def model_builder(hp):
    """Builds a convolutional model."""
    inputs = tf.keras.Input(shape=(155,))
    x = inputs
    for i in range(hp.Int('conv_layers', min_value=3, max_value=10, default=6, step=1)):
        hp_units = hp.Int('hident_units', min_value=32, max_value=512, step=32)
        x = tf.keras.layers.Dense(units=hp_units, activation='relu')(x)

        #x = tf.keras.layers.BatchNormalization()(x)
        #x = tf.keras.layers.ReLU()(x)

    outputs = tf.keras.layers.Dense(60, activation='linear')(x)

    model = tf.keras.Model(inputs, outputs)

    optimizer = hp.Choice('optimizer', ['adam', 'sgd'])
    model.compile(optimizer, loss='mse')
    return model

def main():

    #Change jobNum before moving on to next cell
    jobNum = os.getenv('SLURM_JOBID')  # this will be different for your job. Don't forget to change it!
    user = 'dwalling' # change this to your username!

    #path = '/scratch/' + user + '/job_' + str(jobNum) + '/'
    path = './data/'

    with open(path + 'trainInput.npy', 'rb') as f:
        trainInput = np.load(f)

    with open(path + 'trainOutput.npy', 'rb') as f:
        trainOutput = np.load(f)

    with open(path + 'normConst.npy', 'rb') as f:
        normConst = np.load(f)

    with open(path + 'levs.npy', 'rb') as f:
        levs = np.load(f)

    pressures = levs

    mu = normConst[:,0]
    std = normConst[:,3]

    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

    tuner = kt.RandomSearch(model_builder,
                     objective='val_loss',
                     max_trials=200,
                     #factor=3,
                     directory='results',
                     project_name='keras-tuner-dynamic')

    tuner.search(trainInput, trainOutput, batch_size=1024, epochs=10, validation_split=0.2, callbacks=[stop_early], verbose=2)

def set_environment(num_gpus_per_node="4"):
    nodename = os.environ['SLURMD_NODENAME']
    procid = os.environ['SLURM_LOCALID']
    print(nodename)
    print(procid)
    stream = os.popen('scontrol show hostname $SLURM_NODELIST')
    output = stream.read()
    oracle = output.split("\n")[0]
    print(oracle)
    if procid==num_gpus_per_node:
        os.environ["KERASTUNER_TUNER_ID"] = "chief"
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    else:
        os.environ["KERASTUNER_TUNER_ID"] = "tuner-" + str(nodename) + "-" + str(procid)
        os.environ["CUDA_VISIBLE_DEVICES"] = procid

    os.environ["KERASTUNER_ORACLE_IP"] = oracle + ".expanse.sdsc.edu" #Use full hostname
    os.environ["KERASTUNER_ORACLE_PORT"] = "8000"

if __name__ == '__main__':
    set_environment()
    main()
