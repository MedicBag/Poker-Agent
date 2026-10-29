class Player:
    def __init__(self,bal):
        self.hand = []
        self.balance = bal
        self.game=0

    def set_hand(self,hand):
        self.hand = hand
    def wipe_hand(self):
        self.hand = []

    def play(self,table,numPlayers):
        pass

    def set_game(self,game):
        self.game = game

    def get_hand(self):
        hand=self.hand
        self.hand = []
        return hand
    def get_balance(self):
        return self.balance

    def set_balance(self,balance):
        self.balance = balance
    def fold(self):
        return 0
    def check(self):
        temp=self.game.get_current_bet()
        if self.balance>=temp:
            self.balance-=temp
            return temp
        else:
            temp=self.balance
            self.balance=0
            return temp

    def pay(self,bal):
        if bal>0:
            self.balance+=bal

    def pay_blinds(self,blind):
        if self.balance>=blind:
            self.balance = self.balance-blind
            return blind
        else:
            temp = self.balance
            self.balance=0
            return temp
