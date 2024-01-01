import numpy as np
import pygame
import sys
from .gameBoard import Board
from .pygameUtils import Utils

class TicTacToe:
    def __init__(self,length=600):
        self.length=length
        self.board=Board(self.length)
        self.boardSurf=self.board.getSurf()
        self.screen=None
        
    def gameInit(self):
        pygame.init()
        self.screen=pygame.display.set_mode((600,600))

    def posConvert(self,pos):
        row=pos[1]//(self.board.cellwidth)
        col=pos[0]//(self.board.cellwidth)
        return(3*row+col)

    def playerInput(self,player,machine,state,actions):
        if(player== "Machine"):
            Utils.showmsg(f"Machine's move")
            move=machine.piPolicy(state,actions)
            pygame.time.wait(500)
            return((self.board.step(move),move))
        else:
            Utils.showmsg(f"{player}'s move")
            while(True):
                pos=Utils.displayMouseInput()
                pos=self.posConvert(pos)
                result=self.board.validMove(pos)
                if(result):
                    return((self.board.step(pos),pos))
                else:
                    Utils.showmsg("Invalid Move !!",200)
            
    def show(self):
        self.screen.blit(self.boardSurf,(0,0))
        pygame.display.flip()


    def game(self,machine):
        winner=None
        self.gameInit()
        Utils.showmsg("Starting Tic-Tac-Toe Game",200)
        self.show()
        while(True):
            Utils.showmsg("Enter No.of player 1 or 2")
            n=Utils.keyboardInput()
            if(n=="1" or n=="2"):
                n=int(n)
                break
            else:
                Utils.showmsg("Invalid input !! ",200)
        if(n==1):
            while(True):
                Utils.showmsg(" Do you want to start first ?  click Y or N")
                val=Utils.keyboardInput()
                if(val=="y" or val=="n"):
                    break
                else:
                    Utils.showmsg("Invalid input !! ",200)
            if(val=="y"):
                xPlayer="Your"
                oPlayer="Machine"
            else:
                xPlayer="Machine"
                oPlayer="Your"
        else:
            xPlayer="X player"
            oPlayer="O player"
        state,actions=self.board.state(),self.board.avaliableMoves()
        prevstateFormachine=moveFrommachine=nxtstateFormachine=None
        while(True):
            prevstate=state
            info,move=self.playerInput(xPlayer,machine,state,actions)
            _,reward,state,actions=info
            self.show()
            result=info[0]
            if(xPlayer=="Machine"):
                if(prevstateFormachine!=None):
                    machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine,nxtstateFormachine)
                prevstateFormachine=prevstate
                moveFrommachine=move
                rewardFormachine=reward
                nxtstateFormachine=state
            if(result[0]):
                outcome=result[-1]
                if(outcome in ["X","O"]):
                    winner = xPlayer if (outcome=="X") else oPlayer
                    self.board.showWinningMove(result[1])
                    if(winner=="Your"):
                        winner="You"
                    Utils.showmsg(f"{winner} won the match")
                    if(prevstateFormachine!=None):
                        if(xPlayer!="Machine" and outcome=="X"):
                            machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine-1,nxtstateFormachine)
                        else:
                            machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine+1,nxtstateFormachine)
      
                else:
                    if(xPlayer=="Machine"):
                        machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine-1,nxtstateFormachine)
                    Utils.showmsg("Nomoves! No winner")
                self.show()
                break
            prevstate=state
            info,move=self.playerInput(oPlayer,machine,state,actions)
            self.show()
            _,reward,state,actions=info
            result=info[0]
            if(oPlayer=="Machine"):
                if(prevstateFormachine!=None):
                    machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine,nxtstateFormachine)
                prevstateFormachine=prevstate
                moveFrommachine=move
                rewardFormachine=reward
                nxtstateFormachine=state
            if(result[0]):
                outcome=result[-1]
                if(outcome in ["X","O"]):
                    winner = oPlayer if (outcome=="O") else xPlayer
                    self.board.showWinningMove(result[1])
                    if(winner=="Your"):
                        winner="You"
                    Utils.showmsg(f"{winner} won the match")
                    if(prevstateFormachine!=None):
                            if(oPlayer!="Machine" and outcome=="O"):
                                machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine-1,nxtstateFormachine)
                            else:
                                machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine+1,nxtstateFormachine)

                else:
                    if(oPlayer=="Machine"):
                        machine.state_action_update(prevstateFormachine,moveFrommachine,rewardFormachine-1,nxtstateFormachine)
                    Utils.showmsg("Nomoves! No winner")
                self.show()
                break
           
                
        print(f"{winner} won the match")
        if(xPlayer=="Machine" or oPlayer=="Machine"):
            machine.jsonWrite()
        while(True):
            for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                    print("Window Killed")
                    pygame.quit()
                    sys.exit()   
       
       

            
        

            
        


