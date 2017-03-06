#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:10:25 2017

@author: tobias
"""


from multiprocessing.connection import Client
import numpy as np

address = ('localhost', 4001)
conn = Client(address, authkey=b'secret password')


errorCounter=0
winCounter=0


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
