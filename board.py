#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:59:21 2017

@author: tobias
"""

from multiprocessing.connection import Listener
#from multiprocessing.connection import Client
import numpy as np



turnOnPlayer=1
boardStatus=np.zeros((7,6))
msgP1=''
msgP2=''

gameRun=True
gameCounter=0

numOfGames=int(input('How many games should be played: '))
def newBoard():
    boardStatus=np.zeros((7,6))
    print(boardStatus.T)
    return boardStatus

def checkLeg(boardStatus,move,player):
    legit=False
    if 1<=move<=7:
        legit=True
    if sum(boardStatus[move-1,:]==0)==0:
        legit=False
    if legit==False:
        player.send(-1)
    return legit

def makeMove(boardStatusTemp,move,playerID):
    boardStatusTemp[move-1,6-sum(boardStatus[move-1,:]==0)]=playerID                
    return boardStatusTemp





def checkWin(boardStatus,playerID):
    height=boardStatus.shape[1]
    width=boardStatus.shape[0]    
    #vertical checking
    for row in range(0,height-3):
        for col in range(0,width):
            if (boardStatus[col,row] == playerID and boardStatus[col,row+1] == playerID and boardStatus[col,row+2] == playerID and boardStatus[col,row+3] == playerID):
                return True;
                    
    #horizontal checking
    for row in range(0,height):
        for col in range(0,width-3):
            if (boardStatus[col,row] == playerID and boardStatus[col+1,row] == playerID and boardStatus[col+2,row] == playerID and boardStatus[col+3,row] == playerID):
                return True;
                  
    #row ascending check
    for row in range(0,height-3):
        for col in range(0,width-3):
            if (boardStatus[col,row] == playerID and boardStatus[col+1,row+1] == playerID and boardStatus[col+2,row+2] == playerID and boardStatus[col+3,row+3] == playerID):
                return True;        
    
    
    #row descending check
    for row in range(3,height):
        for col in range(0,width-3):
            if (boardStatus[col,row] == playerID and boardStatus[col+1,row-1] == playerID and boardStatus[col+2,row-2] == playerID and boardStatus[col+3,row-3] == playerID):
                return True;        
    

    return False






print('Four-Connect board is started. Player 1 please connect to port 4001')
address = ('127.0.0.1', 4001)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')
player1 = listener.accept()
print('connection accepted from', listener.last_accepted)
print('Player 1 is connected. Player 2 please connect to port 4001')
player2 = listener.accept()
print('connection accepted from', listener.last_accepted)
print('Player 2 is connected')


def newGame(player1,player2):
    boardStatus=newBoard()
    if np.random.randint(0,2)==1:
        print('Player 1 starts the game with his first turn.')
        player1.send(boardStatus)    
        turnOnPlayer=1
    else:
        player2.send(boardStatus)
        print('Player 2 starts the game with his first turn.')
        turnOnPlayer=2
    print('New game start. Board clear!')
    print(boardStatus.T)
    remis=False
    return turnOnPlayer,boardStatus,remis


turnOnPlayer,boardStatus,remis=newGame(player1,player2)        
while gameRun:
    if turnOnPlayer==1:
        msgP1 = player1.recv()        
    elif turnOnPlayer==2:
        msgP2 = player2.recv()

    if msgP1 == -10 or msgP2 == -10:
        player1.send(-10)
        player2.send(-10)
        player1.close()
        player2.close()
        print('game was cancelled')
        break
    
    
    if turnOnPlayer==1:
    # do something with msg
        if type(msgP1) ==int:
            
            move=msgP1
            if checkLeg(boardStatus,move,player1):
                boardStatus=makeMove(boardStatus,move,1) #Player ID is 1
                print('Player 1 drops coin in: ',str(msgP1))
                print('Player 2 is on turn now.')                
                player2.send(boardStatus)
                turnOnPlayer=2
            else:
                player2.send(0)
                
    elif turnOnPlayer==2:
        if type(msgP2) ==int:
            move=msgP2
            if checkLeg(boardStatus,move,player2):
                boardStatus=makeMove(boardStatus,move,-1) #Player ID is 1
                print('Player 2 drops coin in: ',str(msgP1))
                print('Player 1 is on turn now.')
                player1.send(boardStatus)
                turnOnPlayer=1
            else:
                player1.send(0)
    
    print('BoardStatus is now:')
    print(boardStatus.T)
    
    if np.sum(boardStatus==0)==0:
        remis=True
    
    if remis:
        player1.send(0)
        player2.send(0)
        turnOnPlayer,boardStatus,remis=newGame(player1,player2) 
        gameCounter+=1
        if gameCounter>=numOfGames:
            gameRun=False
            player1.send(-20)
            player2.send(-20)
            
    if (checkWin(boardStatus,1) or checkWin(boardStatus,-1)):        
        if checkWin(boardStatus,1):
            print('Player 1 won the game!!!')
            player1.send(1)
            player2.send(0)                    
        else:
            print('Player 2 won the game!!!')    
            player2.send(1)
            player2.send(0)        
        turnOnPlayer,boardStatus,remis=newGame(player1,player2) 
        gameCounter+=1
        if gameCounter>=numOfGames:
            gameRun=False
            player1.send(-20)
            player2.send(-20)

    

listener.close()