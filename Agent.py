import copy
from Player import Player
import Hand_Eval
import random
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import time

class Agent(Player):

    def __init__(self,bal,sample_size,sample_size_hand,numThreads):
        super().__init__(bal)
        self.deck=[]
        self.deckRegenerate()
        self.game=0
        self.sample_size=sample_size
        self.sample_size_hand=sample_size_hand
        self.numThreads=numThreads
        self.executor = ProcessPoolExecutor(max_workers=numThreads)


    def deckRegenerate(self):
        self.deck=[]
        for x in range(0,4):
            for y in range(1,14):
                self.deck.append((x,y))

    def print_hand(self,hand):
        string =f""
        for x in hand:
            string += self.card_str(x)
            string += " "
        return string

    def card_str(self,card):
        suit=card[0]
        rank=card[1]
        ranks = {1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8",
                 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K", 13: "A"}
        suits = {0: "♥", 1: "♦", 2: "♣", 3: "♠"}
        return f"{ranks.get(rank, '?')}{suits.get(suit, '?')}"


    def play(self,table,numPlayers):
        self.deckRegenerate()

        for card in self.hand:
            self.deck.remove(card)
        for card in table:
            self.deck.remove(card)

        wr=self.eval(table,numPlayers)

        #make bets based off win rate
        if wr>=.52:
            print("big")
            print()
            return self.big_bet()
        if wr>=(1/numPlayers)+.05:
            print("small")
            print()
            return self.small_bet()
        if wr>=(1/numPlayers):
            print("check")
            print()
            return self.check()
        else:
            print("fold")
            print()
            return self.fold()

    def big_bet(self):
        temp=max(self.game.get_pot_size(),100)
        if self.balance>=temp:
            self.balance-=temp
            return temp
        else:
            temp=self.balance
            self.balance=0
            return temp


    def small_bet(self):
        temp = max(self.game.get_min_bet(),self.game.get_pot_size()*.2,self.game.get_current_bet())
        if self.balance >= temp:
            self.balance -= temp
            return temp
        else:
            temp = self.balance
            self.balance = 0
            return temp


    def fold(self):
        return 0

    #method to get monte carlo samples
    def get_sample_hands(self, length, num):
        unique_hands = set()
        while len(unique_hands) < num:
            new_hand = random.sample(self.deck, length)
            unique_hands.add(tuple(new_hand))
        return [list(hand) for hand in unique_hands]

    # method to evaluate hand
    def eval(self,table,numPlayers):

        temp_sample_size=self.sample_size
        if (table==[]):
            temp_sample_size=self.sample_size_hand

        samples=self.get_sample_hands((5-len(table)+(2*numPlayers)),temp_sample_size)
        scores=[]

        for x in range(0,numPlayers):
            scores.append(0)

        temphand=copy.deepcopy(self.hand)
        batch_size = max(1, len(samples) // self.numThreads)
        chunks = [samples[i:i + batch_size] for i in range(0, len(samples), batch_size)]

        start = time.time()
        fn = partial(threadtask, table, numPlayers,temphand)
        results = list(self.executor.map(fn, chunks))


        for result in results:
            for winner_indexs in result:
                for index in winner_indexs:
                    scores[index]+=1

        print(f"Evaluation took {time.time() - start:.3f}s")

        for x in range(0,numPlayers):
            print(f"player {x} : {scores[x]}")
            if x==0:
                print("Hand:")
                print(self.print_hand(self.hand))
                print("Table Cards:")
                print(self.print_hand(table))
                print(f"Win Rate: {scores[x]/len(samples)}" )
        print("")
        return scores[0]/len(samples)

    #method to assign threads to loop through chunks
def threadtask(table,numPlayers,hand,combs):
    winners=[]
    for x in combs:
        winners.append(sample_eval(table,numPlayers,x,hand))
    return winners

    # part that actually calls the Hand Eval file
def sample_eval(table,numPlayers,comb,hand):
    temp_table=copy.deepcopy(table)
    temp_hands=[copy.deepcopy(hand)]
    temp_scores=[]
    for x in range(0,5-len(temp_table)):
        temp_table.append(comb[0])
        comb.pop(0)

    for x in range(0,numPlayers-1):
        temp_hands.append(copy.deepcopy([comb[0],comb[1]]))
        comb.pop(0)
        comb.pop(0)

    full_hands=[hand +temp_table for hand in temp_hands]
    for x in full_hands:
        temp_scores.append(Hand_Eval.hand_eval(x))
    winner=max(temp_scores)
    winner_ids=[]
    for i, score in enumerate(temp_scores):
         if score == winner:
             winner_ids.append(i)
    return winner_ids
