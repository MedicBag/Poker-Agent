import copy
import random
from traceback import print_tb

import Hand_Eval

class Poker():
    def __init__(self, players,min_bet):
        self.players = players
        self.min_bet = min_bet
        self.dealer=0
        self.deck=[]
        self.table=[]
        self.pot_size=0
        self.side_pots=[]
        self.current_bet=0

        self.deckRegenerate()
        for x in players:
            x.set_game(self)

    def deckRegenerate(self):
        self.deck=[]
        for x in range(0,4):
            for y in range(1,14):
                self.deck.append((x,y))

    def set_table_cards(self,num):
        for x in range(0,num):
            temp= random.randint(0, len(self.deck) - 1)
            self.table.append(copy.deepcopy(self.deck[temp]))
            self.deck.pop(temp)

    def reset(self):
        self.deckRegenerate()
        self.table=[]
        self.pot_size=0
        self.current_bet=0

    def get_table_cards(self):
        return self.table

    def get_min_bet(self):
        return self.min_bet

    def get_pot_size(self):
            return self.pot_size

    #used for testing
    def forceplay(self,num):
        self.players[num].play(self.table,len(self.players))

    def deal(self):
        for x in self.players:
            hand = []
            for y in range(0,2):
                temp = random.randint(0, len(self.deck) - 1)
                hand.append(copy.deepcopy(self.deck[temp]))
                self.deck.pop(temp)
            x.set_hand(hand)

    def get_current_bet(self):
        return self.current_bet

    def update_pot_size(self,bets):
        self.pot_size=sum(bets)

    def round(self):

        self.deal()
        in_hand=[]
        redo=False
        player_bets = []
        scores=[]
        folded = []
        for x in self.players:
            player_bets.append(0)
            scores.append(0)

        for x in range(len(self.players)):
            in_hand.append( (self.dealer+1+x) % (len(self.players) ))

        for y in range(0,4):
            if(len(in_hand)<=1):
                break
            for x in in_hand:
                self.update_pot_size(player_bets)
                print(f"Amount Needed to call: {self.current_bet-player_bets[x]}" )
                player_bets[x]+=(self.players[x].play(self.table,len(in_hand)))
                if player_bets[x]==0 and self.players[x].get_balance()!=0 :
                    folded.append(x)
                else:
                    if player_bets[x]>self.current_bet:
                        self.current_bet=player_bets[x]
                        redo=True
                        folded=[]

            if len(folded)==len(in_hand):
                folded=[]
            for x in folded:
                in_hand.remove(x)
            folded=[]

            while redo:
                redo=False
                for x in in_hand:
                    self.update_pot_size(player_bets)
                    print(f"Amount Needed to call: {self.current_bet - player_bets[x]}")
                    if player_bets[x]<self.current_bet:
                        temp=player_bets[x]
                        player_bets[x]+=self.players[x].play(self.table,len(in_hand))
                        if player_bets[x]>self.current_bet:
                            redo=True
                            self.current_bet=player_bets[x]
                        elif(temp==player_bets[x] and self.players[x].get_balance()!=0):
                            folded.append(x)
                if len(folded)==len(in_hand):
                    folded=[]
                for x in folded:
                    in_hand.remove(x)
                folded = []





            if y==0 :
                self.set_table_cards(3)
            elif y!=3:
                self.set_table_cards(1)

        print(f" Table Cards: {print_hand(self.table)} ")
        for x in in_hand:
            temp=copy.deepcopy(self.table)

            for i in self.players[x].get_hand():
                temp.append(i)
            print(f"Player {x} had {print_hand(temp[-2:])}")
            scores[x]+=Hand_Eval.hand_eval(temp)

        winner = max(scores)
        winners=[]
        for x in in_hand:
            if scores[x]==winner:
                winners.append(x)


        self.payout(winners,sum(player_bets))
        self.cut()
        self.update_dealer()
        self.reset()

    #removes players without money
    def cut(self):
        for x in range(len(self.players)-1,-1,-1):
            if self.players[x].balance <= 0:
                self.players.pop(x)

    def payout(self,winners,sum):
        for x in winners:
            self.players[x].pay(sum/len(winners))
        self.pot_size=0

    #moves dealer index
    def update_dealer(self):
        self.dealer+=1
        if self.dealer>len(self.players)-1:
            self.dealer=0

    # initiates game
    def game(self):
        while(len(self.players)>1):
            self.round()

def print_hand(hand):
    string =f""
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