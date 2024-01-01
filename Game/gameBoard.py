import numpy as np
import pygame
from .pygameUtils import Utils
class Board:
    def __init__(self,length=600) -> None:
        self.boardData=np.full((3,3),None)
        self.length=length
        self.sym="X"
        self.boardSurf=pygame.Surface((self.length,self.length))
        self.cellwidth=(self.length)//3
        self.centers=np.array([((j * self.cellwidth) + (self.cellwidth / 2), ((i * self.cellwidth) + (self.cellwidth / 2))) for i in range(3) for j in range(3)])
        self.boardInit()

    def boardInit(self):
        self.boardSurf.fill((255,255,255))
        self.drawBoard()

    def state(self):
        temp=list()
        for row in range(3):
            for col in range(3):
                val=self.boardData[row][col]
                if(val!=None):
                    temp.append(val)
                else:
                    temp.append(" ")
        return("".join(temp))



    def reset(self):
        self.boardInit()
        self.boardData=np.full((3,3),None)
        self.sym="X"
        
    
    def avaliableMoves(self):
        return([i for i,j in enumerate(self.boardData.flatten()) if j==None])

    def drawBoard(self):
        for i in range(1,3):
            Utils.drawBlackLine(self.boardSurf,(i*self.cellwidth,0),(i*self.cellwidth,self.length))
            Utils.drawBlackLine(self.boardSurf,(0,i*self.cellwidth),(self.length,i*self.cellwidth))

    def mirrorDataToSurf(self):
        for sym,pos in zip(self.state(),self.centers):
            if(sym=="X"):
                Utils.drawX(self.boardSurf,pos,0.2*self.cellwidth)
            elif(sym=="O"):
                Utils.drawO(self.boardSurf,pos,0.3*self.cellwidth)

    def validMove(self,pos):
        x,y=(pos//3),(pos%3)
        if(self.boardData[x][y]!=None):
            return(False)
        return(True)

    def getSurf(self):
        return(self.boardSurf)
    

    def step(self,pos):
        x,y=(pos//3),(pos%3)
        prstsym=self.sym
        self.sym="O" if (self.sym=="X") else "X"
        nxtsym=self.sym
        self.boardData[x][y]=nxtsym
        nxtcheckval=self.check(nxtsym)
        reward=0
        if(nxtcheckval[0]):
            if(nxtcheckval[2]==nxtsym):
                reward=0.5
        self.boardData[x][y]=prstsym
        prstcheckval=self.check(prstsym)
        if(prstcheckval[0]):
            if(prstcheckval[2]==prstsym):
                reward=1
        self.mirrorDataToSurf()
        return((prstcheckval,reward,self.state(),self.avaliableMoves()))
    

    
    def check(self,sym):
        def helper(sym):
            vecfunc=np.vectorize(lambda x,v:x==v)
            boolv=vecfunc(self.boardData,sym)
            boolOR=np.all(boolv,axis=1)
            boolOC=np.all(boolv,axis=0)
            boolMD=np.diagonal(boolv)
            boolPD=np.diagonal(np.rot90(boolv))
            for i,j in enumerate(boolOR):
                if(j):
                    return((True,i,sym))
            for i,j in enumerate(boolOC):
                if(j):
                    return((True,(3+i),sym))
            if(np.all(boolMD)):
                return((True,-1,sym))
            elif(np.all(boolPD)):
                return(True,-2,sym)
            else:
                return((False,None,None))
        SymCheck=helper(sym)
        if(SymCheck[0]):
            return(SymCheck)
        if(not self.avaliableMoves()):
            return((True,None,"noMoves"))
        return((False,None,None))
    
    def showWinningMove(self,winnermove):
        if(winnermove==0):
            strt=self.centers[0]
            ends=self.centers[2]
        if(winnermove==1):
            strt=self.centers[3]
            ends=self.centers[5]
        if(winnermove==2):
            strt=self.centers[6]
            ends=self.centers[8]
        if(winnermove==3):
            strt=self.centers[0]
            ends=self.centers[6]
        if(winnermove==4):
            strt=self.centers[1]
            ends=self.centers[7]
        if(winnermove==5):
            strt=self.centers[2]
            ends=self.centers[8]
        if(winnermove==-1):
            strt=self.centers[0]
            ends=self.centers[8]
        if(winnermove==-2):
            strt=self.centers[2]
            ends=self.centers[6]
        if(winnermove!=None):
            Utils.drawBlueLine(self.boardSurf,strt,ends)

    def render(self):
        return np.rot90(pygame.surfarray.array3d(self.boardSurf),k=3)






    