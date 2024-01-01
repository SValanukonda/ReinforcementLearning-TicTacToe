from Model.model import Agent
from Game.gameEnv import TicTacToe

game = TicTacToe()
model=Agent("Model_Alpha")
# loading already trained model
model.jsonload()
game.game(model) 