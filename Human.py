from logging import exception
import os
from Player import Player


class Human(Player):
    def __init__(self,bal):
        super().__init__(bal)

    def play(self,table,numPlayers):
        current_bet=self.game.get_current_bet()

        while True :

            print(f"Hand Cards:{print_hand(self.hand)}")
            print(f"Table Cards:{print_hand(table)}")
            print(f"Number of Players: {numPlayers}")
            print(f"Minimum Bet: {self.game.get_min_bet()}")
            print(f"Current Bet: {current_bet}")
            print(f"Balance: {self.balance}")
            print("Input desired bet (0 to fold/check)")

            value=input()
            try:
                value = int(value)
                if value<= self.balance:
                    self.balance -= value
                    return value
                else:
                    print("Invalid input")
            except ValueError:
                print("Please input a valid integer")




def print_hand(hand):
    string =f""
    if hand==[]:
        return
    for x in hand:
        string += card_str(x)
        string += " "
    return string

def card_str(card):
    suit=card[0]
    rank=card[1]
    ranks = {1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8",
                 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K", 13: "A"}
    suits = {0: "♥", 1: "♦", 2: "♣", 3: "♠"}
    return f"{ranks.get(rank, '?')}{suits.get(suit, '?')}"