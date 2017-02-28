#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:10:25 2017

@author: tobias
"""


#import gc
##import keras
#from keras.models import Sequential, Model
##from keras.optimizers import SGD
#from keras.regularizers import l2,l1 #, activity_l2,activity_l1
#from keras.layers import Dense, Input, Dropout, Activation
#from keras.layers.advanced_activations import LeakyReLU,PReLU, ELU,SReLU
#from keras.layers.recurrent import LSTM
#from keras.engine.topology import Merge
#from keras.callbacks import EarlyStopping
#from keras import backend as K
#from keras.callbacks import ModelCheckpoint
#from keras.layers.convolutional import Conv1D
#from keras.layers.core import Flatten
#from scipy.stats.mstats import zscore
from multiprocessing.connection import Client
import numpy as np

address = ('localhost', 4001)
conn = Client(address, authkey=b'secret password')


errorCounter=0
winCounter=0

#from itertools import compress

#import tensorflow as tf
#
##Misc Imports
#import h5py
##import yaml
#import scipy.io as io

#import random
#import sys
#import time
#import platform
#import seq2seq
#from seq2seq.models import SimpleSeq2Seq
#from seq2seq.models import Seq2Seq as SS

def checkLeg(boardStatus,move):
    legit=False
    if 1<=move<=7:
        legit=True
    if sum(boardStatus[move-1,:]==0)==0:
        legit=False
    return legit
        


while True:    
    msg=conn.recv()
    if type(msg)==np.ndarray:
        boardStatus=msg
        print('')
        print('actual BoardStatus:')
        print(boardStatus.T)
        print('what move do you want to make (1-7)')
        legit=False
        while legit==False:
            move=np.random.randint(1,8)
            legit=checkLeg(boardStatus,move)
#        move=input('Move: ')
        
        conn.send(int(move))
        if move==-10:
            conn.close()
            break
    elif type(msg)==int:
        if msg==-1:
            errorCounter+=1
        elif msg==1:
            winCounter+=1
            print(winCounter,' Wins already =)')
        elif msg==-10:
            conn.close()
            break
#conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
#conn.close()