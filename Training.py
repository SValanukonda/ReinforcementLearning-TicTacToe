from Game.gameBoard import Board
from Model.model import Agent
from matplotlib import pyplot as plt
import numpy as np
import time 
import pygame

ouputfile=open("output.txt","w")
tictactoe=Board()
modelA=Agent("Model_Alpha")
modelB=Agent("Model_Beta")
Visualize=False
episodes=10_00_000
screen=None
if(Visualize):
    pygame.init()
    screen=pygame.display.set_mode((600,600))

def show(screen):
    if(Visualize):
        tictactoe.mirrorDataToSurf()
        board=tictactoe.getSurf()
        screen.blit(board,(0,0))
        pygame.display.flip()
        pygame.time.wait(500)


stateActionGains={
    modelA.name:dict(),
    modelB.name:dict()
}

woncount={
    modelA.name:0,
    modelB.name:0
}

ecount=0
for i in range(episodes):
    done = False
    tictactoe.reset()
    curr_state=tictactoe.state()
    actions=tictactoe.avaliableMoves()
    show(screen)
    firstmodel,secondmodel=np.random.permutation([modelA,modelB])
    ouputfile.write(f"model order -- 1.{firstmodel.name} 2.{secondmodel.name} \n")
    winner=None
    prevstateForSecondmodel=prevstateForFirstmodel=None
    while(done==False):
        prevstateForFirstmodel=curr_state
        moveFromFirstmodel=firstmodel.policy(curr_state,actions)
        # print(f"move taken={moveFromFirstmodel}")
        check,rewardForFirstmodel,nxtstateFromFirstmodel,actions=tictactoe.step(moveFromFirstmodel)
        curr_state=nxtstateFromFirstmodel
        show(screen)
        if(check[0]):
            if(check[-1]=="X"):
                winner=firstmodel.name
                firstmodel.state_action_update(prevstateForFirstmodel,moveFromFirstmodel,rewardForFirstmodel+1,nxtstateFromFirstmodel)
            else:
                firstmodel.state_action_update(prevstateForFirstmodel,moveFromFirstmodel,rewardForFirstmodel-1,nxtstateFromFirstmodel)
            secondmodel.state_action_update(prevstateForSecondmodel,moveFromSecondmodel,rewardForSecondmodel-1,nxtstateFromSecondmodel)
            break
        else:
            if(prevstateForSecondmodel!=None):
                secondmodel.state_action_update(prevstateForSecondmodel,moveFromSecondmodel,rewardForSecondmodel,nxtstateFromSecondmodel)

        prevstateForSecondmodel=curr_state
        moveFromSecondmodel=firstmodel.policy(curr_state,actions)
        check,rewardForSecondmodel,nxtstateFromSecondmodel,actions=tictactoe.step(moveFromSecondmodel)
        show(screen)
        # print(f"move taken={moveFromSecondmodel}")
        if(check[0]):
            if(check[-1]=="O"):
                winner=secondmodel.name
                secondmodel.state_action_update(prevstateForSecondmodel,moveFromSecondmodel,rewardForSecondmodel+1,nxtstateFromSecondmodel)
            else:
                secondmodel.state_action_update(prevstateForSecondmodel,moveFromSecondmodel,rewardForSecondmodel-1,nxtstateFromSecondmodel)
            firstmodel.state_action_update(prevstateForFirstmodel,moveFromFirstmodel,rewardForFirstmodel-1,nxtstateFromFirstmodel)
            break
        else:
            firstmodel.state_action_update(prevstateForFirstmodel,moveFromFirstmodel,rewardForFirstmodel,nxtstateFromFirstmodel)

    ecount+=1
    if(winner!=None):
        woncount[winner]+=1
        ouputfile.write(f"{winner} won the match with value ={check} \n")
    else:
        ouputfile.write(" None won \n")
    
    ouputfile.write(f"completed {ecount} episode \n")
    time.sleep(0.1)


show(screen)
if(Visualize):
    a=input("Please enter any key to close screen \n")
    pygame.quit()
modelA.jsonWrite()
modelB.jsonWrite()
ouputfile.write("writing completed \n")
ouputfile.write(str(woncount))

   


    


