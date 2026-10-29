from Agent import Agent
from Player import Player
from Poker import Poker
# agent takes (balance, sample size, sample size when only 2 cards, number of threads)
players=[Agent(700,100000,10000,10),Player(700),Player(700),Player(700)]
game=Poker(players,10)
game.deal()
game.set_table_cards(3) #used to set number of cards on table when evaluating
if __name__ == '__main__':
    game.forceplay(0)
