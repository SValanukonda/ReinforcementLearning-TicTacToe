import numpy as np
import json
import random
class Agent:
    def __init__(self,name) -> None:
        self.name=name
        self.state_action=dict()
    

    def state_action_update(self,state,action,reward,nxtstate,alpha=0.1,gamma=0.99):
        # print(f"in update func --- state- {state} - reward- {reward}")
        if(state not in self.state_action.keys()):
            self.state_action[state]=[0 for _ in range(9)]
        if(nxtstate not in self.state_action.keys()):
            self.state_action[nxtstate]=[0 for _ in range(9)]
        # print(f"state={state}-action={action} reward-{reward}")
        # print(f"before={self.state_action[state][action]}")
        self.state_action[state][action]=self.state_action[state][action]+alpha*(reward+gamma*(max(self.state_action[nxtstate]))-self.state_action[state][action])
        # print(f"after={self.state_action[state][action]}")

        
            
    def policy(self,state,actions):
        if(state not in self.state_action.keys()):
            prob=[0 for _ in range(9)]
            self.state_action[state]=prob
        
        val=max([self.state_action[state][i] for i in actions])
        poa=list()
        poz=list()
        for i in actions:
            if(self.state_action[state][i]==val):
                poa.append(i)
            if(self.state_action[state][i]==0):
                poz.append(i)
        if(poz):
            return(np.random.choice(poz))
        else:
            return(self.piPolicy(state,actions))
        
    def piPolicy(self,state,actions,epsilon=-1):
        # print("In pi Policy func")
        if(state not in self.state_action.keys()):
            self.state_action[state]=[0 for _ in range(9)]
        # print(f"#{state}#--{self.state_action[state]}")
        # print(f"actions--{actions}")
        val=random.random()
        if(val<=epsilon):
            print("random selection:--")
            return(np.random.choice(actions))
        else:
            val=max([self.state_action[state][i] for i in actions])
            poa=list()
            for i in actions:
                if(self.state_action[state][i]==val):
                    poa.append(i)
            return(np.random.choice(poa))
              


    def jsonload(self):
        print(f"./Data/{self.name}+_action_fuction_+.json")
        with open("./Data/"+self.name+"_action_fuction_"+".json","r") as inpt1:
            self.state_action=json.load(inpt1)
        print(f"loaded....length={len(self.state_action)}")


    def jsonWrite(self):
        with open("./Data/"+self.name+"_action_fuction_"+".json","w") as output1:
            json.dump(self.state_action,output1,indent=4)
        print(f"json file created for {self.name}")