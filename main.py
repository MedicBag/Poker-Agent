from Agent import Agent
from Human import Human
from Poker import Poker

players=[Agent(700,100000,10000,10),Agent(700,100000,10000,10),Agent(700,100000,10000,10),Human(700,)]
game=Poker(players,10)
if __name__ == '__main__':
    game.game()