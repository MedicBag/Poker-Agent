import copy
from copy import deepcopy


def get_kickers(hand, num, used, offset):
    kickers = [card for card in hand if card[1] not in used]
    value = 0
    for i in range(1, num + 1):
        value += (.01 ** i) * kickers[-i][1]
    return value * (.01 ** offset)

def straight_prep(hand):
    for x in hand[-3:]:
        if x[1]==13:
            hand.insert(0,(x[0],0))
    return hand

def is_royalflush(hand):
    for x in range(0, 4):
        count = 0
        used = []
        for y in hand:
            if y[0] == x:
                count += 1
                used.append(y[1])
        if len(used) >= 5:
            if used[-5:]==[9,10,11,12,13]:
                return 10

    return -1

def is_straight(hand):
    hand=straight_prep(hand)
    used=[]
    current = hand[0][1] - 1
    max=-1
    doubles=0
    for x in hand:
        if (x[1] !=current+1) and(x[1] !=current):
            used=[x]
            doubles=0
            current = x[1]
            continue
        else:
            used.append(x)
            if (x[1] ==current):
                doubles += 1
        current=x[1]
        if (len(used)-doubles>=5):
            max = used[-1][1]
    if max!=-1:
        return 5+(.01*max)
    return -1




def is_flush(hand):


    for x in range(0, 4):
        used = []
        for y in hand:
            if y[0] == x:
                used.append(y[1])
        if len(used)>=5:
            value=0
            for i in range(1,6):
                value+= (.01**(i))*used[-1*i]
            return 6 + value

    return-1

def is_straight_flush(hand):
    for x in range(0, 4):
        used = []
        for y in hand:
            if y[0] == x:
                used.append(y)
        if len(used)>=5:
            temp=is_straight(used)
            if temp!=-1:
                return 9+(temp-5)
            return -1
    return -1

def is_full_house(hand):
    upper = -1
    lower = -1
    for x in range(13,0,-1):
        count =0
        for y in hand:
            if y[1]==x:
                count += 1
        if count==3:
            upper=x
            break
    if upper==-1:
        return -1

    for x in range(len(hand)-1,-1,-1):
        if hand[x][1]==upper:
            hand.pop(x)

    for x in range(13,0,-1):
        count =0
        for y in hand:
            if y[1]==x:
                count += 1
        if count>=2:
            lower=x
            return 7+(.01*upper)+(.0001*lower)
    return-1



def four_of_a_kind(hand):
    for x in range(13,0,-1):
        count=0
        for y in hand:
            if y[1]==x:
                count+=1
        if count==4:
            return 8+(.01*x)+get_kickers(hand,1,[x],1)
    return-1


def three_of_a_kind(hand):
    for x in range(13,0,-1):
        count=0
        for y in hand:
            if y[1]==x:
                count+=1
        if count==3:
            return 4+(.01*x)+get_kickers(hand,2,[x],1)
    return -1

def two_pair(hand):
    upper=-1
    lower=-1
    for x in range(1,14):
        count=0
        for y in hand:
            if y[1] == x:
                count += 1
        if count == 2:
            if upper != -1:
                lower=upper
                upper = x
            else:
                upper = x
    if lower!=-1:
        return 3+(.01*upper)+(.0001*lower)+get_kickers(hand,1,[upper,lower],2)
    return -1



def one_pair(hand):
    for x in range(13, 0, -1):
        count = 0
        for y in hand:
            if y[1] == x:
                count += 1
                if count==2:
                    return 2 + (.01 * x) + get_kickers(hand,3,[x],1)

    return -1




def hand_eval(hand):
    checks =[
        is_royalflush,
        is_straight_flush,
        four_of_a_kind,
        is_full_house,
        is_flush,
        is_straight,
        three_of_a_kind,
        two_pair,
        one_pair,
    ]
    hand.sort(key=lambda x: x[1])
    for check in checks:
        score =check(copy.deepcopy(hand))
        if score!=-1 :
            return score
    return 1+get_kickers(hand,5,[],0)



cards = {
    0: "Ace",
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "10",
    10: "Jack",
    11: "Queen",
    12: "King",
    13: "Ace"
}
suits = {
    0: "Hearts",
    1: "Diamonds",
    2: "Clubs",
    3: "Spades"
}
hand_rankings = {
    1: "High Card",
    2: "One Pair",
    3: "Two Pair",
    4: "Three of a Kind",
    5: "Straight",
    6: "Flush",
    7: "Full House",
    8: "Four of a Kind",
    9: "Straight Flush",
    10: "Royal Flush"
}

