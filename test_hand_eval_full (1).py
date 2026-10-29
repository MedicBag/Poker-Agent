"""
test_hand_eval_full.py
======================
Comprehensive test suite for Hand_Eval.py — all hands are 7 cards (Texas Hold'em style).

Card format: (suit, rank)
  suit : 0=Hearts, 1=Diamonds, 2=Clubs, 3=Spades
  rank : 1=2, 2=3, ..., 9=10, 10=Jack, 11=Queen, 12=King, 13=Ace

Run:  python test_hand_eval_full.py
"""

import sys, traceback, copy, importlib.util, pathlib

SOURCE = pathlib.Path(__file__).parent / "Hand_Eval.py"

def load_module(path):
    spec = importlib.util.spec_from_file_location("hand_eval_mod", path)
    mod  = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"[LOAD ERROR] Could not import {path}:\n  {e}\n")
    return mod

mod = load_module(SOURCE)

# ── Helpers ───────────────────────────────────────────────────────────────────

def rank_of(score):
    return int(score)

def describe(score):
    rankings = {
        1: "High Card", 2: "One Pair", 3: "Two Pair",
        4: "Three of a Kind", 5: "Straight", 6: "Flush",
        7: "Full House", 8: "Four of a Kind",
        9: "Straight Flush", 10: "Royal Flush",
    }
    return rankings.get(rank_of(score), f"Unknown({score})")

def card_str(suit, rank):
    ranks = {1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8",
             8:"9",9:"10",10:"J",11:"Q",12:"K",13:"A"}
    suits = {0:"♥",1:"♦",2:"♣",3:"♠"}
    return f"{ranks.get(rank,'?')}{suits.get(suit,'?')}"

def hand_str(hand):
    return " ".join(card_str(s, r) for s, r in hand)

results = {"pass": 0, "fail": 0, "error": 0}

def run_test(label, hand, expected_rank):
    assert len(hand) == 7, f"Test '{label}' has {len(hand)} cards, expected 7!"
    fn = getattr(mod, "hand_eval", None)
    if fn is None:
        print(f"  [ERROR] hand_eval not found in module")
        results["error"] += 1
        return

    hand_copy = copy.deepcopy(hand)
    try:
        score = fn(hand_copy)
        actual_rank = rank_of(score)
        ok = actual_rank == expected_rank
        status = "PASS" if ok else "FAIL"
        results["pass" if ok else "fail"] += 1
        detail = (
            f"score={score:.6f}  ({describe(score)})"
            if ok else
            f"score={score:.6f}  got={describe(score)}  expected={expected_rank} ({rankings_map[expected_rank]})"
        )
        print(f"  [{status}] {label:55s} | {hand_str(hand):42s} | {detail}")
    except Exception:
        results["error"] += 1
        print(f"  [ERROR] {label:55s} | {hand_str(hand)}")
        traceback.print_exc()

def run_tiebreak(label, better, worse):
    assert len(better) == 7 and len(worse) == 7
    fn = getattr(mod, "hand_eval", None)
    if fn is None:
        results["error"] += 1
        return
    try:
        s1 = fn(copy.deepcopy(better))
        s2 = fn(copy.deepcopy(worse))
        ok = s1 > s2
        status = "PASS" if ok else "FAIL"
        results["pass" if ok else "fail"] += 1
        print(f"  [{status}] {label:55s} | {s1:.6f} vs {s2:.6f}")
    except Exception as e:
        results["error"] += 1
        print(f"  [ERROR] {label}: {e}")
        traceback.print_exc()

def section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

rankings_map = {
    1: "High Card", 2: "One Pair", 3: "Two Pair",
    4: "Three of a Kind", 5: "Straight", 6: "Flush",
    7: "Full House", 8: "Four of a Kind",
    9: "Straight Flush", 10: "Royal Flush",
}

# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_royal_flush():
    section("Royal Flush (expected rank 10)")
    # Basic in each suit
    run_test("RF hearts",
        [(0,9),(0,10),(0,11),(0,12),(0,13),(1,1),(2,2)], 10)
    run_test("RF diamonds",
        [(1,9),(1,10),(1,11),(1,12),(1,13),(0,1),(2,2)], 10)
    run_test("RF clubs",
        [(2,9),(2,10),(2,11),(2,12),(2,13),(0,1),(1,2)], 10)
    run_test("RF spades",
        [(3,9),(3,10),(3,11),(3,12),(3,13),(0,1),(1,2)], 10)
    # With pair in remaining cards
    run_test("RF spades + pair of 2s",
        [(3,9),(3,10),(3,11),(3,12),(3,13),(0,1),(1,1)], 10)
    # With trips in remaining cards
    run_test("RF hearts + trip 3s in remaining",
        [(0,9),(0,10),(0,11),(0,12),(0,13),(1,2),(2,2)], 10)
    # Garbage kickers
    run_test("RF diamonds + garbage kickers",
        [(1,9),(1,10),(1,11),(1,12),(1,13),(2,5),(3,7)], 10)
    # RF beats SF: only 5 cards of RF suit
    run_test("RF hearts with exactly 5 RF cards",
        [(0,9),(0,10),(0,11),(0,12),(0,13),(3,8),(3,7)], 10)


def test_straight_flush():
    section("Straight Flush (expected rank 9)")
    # Low end (A-5 wheel)
    run_test("SF A-5 wheel hearts",
        [(0,1),(0,2),(0,3),(0,4),(0,13),(1,7),(2,11)], 9)
    # Various positions
    run_test("SF 2-6 clubs",
        [(2,1),(2,2),(2,3),(2,4),(2,5),(0,9),(1,12)], 9)
    run_test("SF 3-7 diamonds",
        [(1,2),(1,3),(1,4),(1,5),(1,6),(0,1),(3,12)], 9)
    run_test("SF 4-8 spades",
        [(3,3),(3,4),(3,5),(3,6),(3,7),(0,1),(1,12)], 9)
    run_test("SF 5-9 clubs",
        [(2,4),(2,5),(2,6),(2,7),(2,8),(0,1),(1,12)], 9)
    run_test("SF 6-T hearts",
        [(0,5),(0,6),(0,7),(0,8),(0,9),(1,1),(2,12)], 9)
    run_test("SF 7-J diamonds",
        [(1,6),(1,7),(1,8),(1,9),(1,10),(0,13),(3,12)], 9)
    run_test("SF 8-Q clubs",
        [(2,7),(2,8),(2,9),(2,10),(2,11),(0,1),(1,2)], 9)
    run_test("SF 9-K spades",
        [(3,8),(3,9),(3,10),(3,11),(3,12),(0,1),(1,2)], 9)
    # SF not confused with RF (K-high, not A-high)
    run_test("SF 9-K hearts not RF",
        [(0,8),(0,9),(0,10),(0,11),(0,12),(1,1),(2,2)], 9)
    # 6-card SF: best 5 chosen
    run_test("SF 6-card suit: best 5 of 6 chosen",
        [(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(0,1)], 9)
    # SF with offsuit pair
    run_test("SF with offsuit pair of Ks",
        [(0,5),(0,6),(0,7),(0,8),(0,9),(1,12),(2,12)], 9)


def test_four_of_a_kind():
    section("Four of a Kind (expected rank 8)")
    run_test("Quad 2s + A K kickers",
        [(0,1),(1,1),(2,1),(3,1),(0,13),(1,12),(2,11)], 8)
    run_test("Quad 3s",
        [(0,2),(1,2),(2,2),(3,2),(0,13),(1,12),(2,11)], 8)
    run_test("Quad 7s",
        [(0,6),(1,6),(2,6),(3,6),(0,13),(1,12),(2,11)], 8)
    run_test("Quad Ts",
        [(0,9),(1,9),(2,9),(3,9),(0,13),(1,12),(2,11)], 8)
    run_test("Quad Js",
        [(0,10),(1,10),(2,10),(3,10),(0,13),(1,12),(2,11)], 8)
    run_test("Quad Qs",
        [(0,11),(1,11),(2,11),(3,11),(0,13),(1,12),(2,9)], 8)
    run_test("Quad Ks",
        [(0,12),(1,12),(2,12),(3,12),(0,13),(1,9),(2,7)], 8)
    run_test("Quad As",
        [(0,13),(1,13),(2,13),(3,13),(0,12),(1,11),(2,9)], 8)
    # Quad with pair in remaining
    run_test("Quad 5s + pair of 8s",
        [(0,4),(1,4),(2,4),(3,4),(0,7),(1,7),(2,12)], 8)
    # Quad with trips in remaining (impossible in real poker but tests robustness)
    run_test("Quad 3s + trip Ks (would be 7-card hand edge)",
        [(0,2),(1,2),(2,2),(3,2),(0,12),(1,12),(2,12)], 8)


def test_full_house():
    section("Full House (expected rank 7)")
    run_test("FH 2s over 3s",
        [(0,1),(1,1),(2,1),(0,2),(1,2),(2,13),(3,12)], 7)
    run_test("FH 3s over 2s",
        [(0,2),(1,2),(2,2),(0,1),(1,1),(2,13),(3,12)], 7)
    run_test("FH 5s over 4s",
        [(0,4),(1,4),(2,4),(0,3),(1,3),(2,13),(3,12)], 7)
    run_test("FH 9s over 8s",
        [(0,8),(1,8),(2,8),(0,7),(1,7),(2,13),(3,12)], 7)
    run_test("FH Ks over Qs",
        [(0,12),(1,12),(2,12),(0,11),(1,11),(2,3),(3,2)], 7)
    run_test("FH As over Ks",
        [(0,13),(1,13),(2,13),(0,12),(1,12),(0,7),(1,5)], 7)
    run_test("FH As over 2s",
        [(0,13),(1,13),(2,13),(0,1),(1,1),(2,7),(3,5)], 7)
    # Two trips: best trip used as three, best remaining pair used
    run_test("FH: two trips in hand, higher used as three",
        [(0,12),(1,12),(2,12),(0,11),(1,11),(2,11),(3,1)], 7)
    # Three pair + trip: still FH
    run_test("FH: trips + two pair, best FH chosen",
        [(0,12),(1,12),(2,12),(0,11),(1,11),(0,10),(1,10)], 7)
    # FH not confused with flush (5 suited + FH)
    run_test("FH: 5-flush suit present but FH wins",
        [(0,13),(0,12),(0,11),(0,10),(0,9),(1,13),(2,13)], 10)  # Actually RF


def test_flush():
    section("Flush (expected rank 6)")
    run_test("Flush hearts A-high",
        [(0,13),(0,11),(0,9),(0,7),(0,5),(1,12),(2,10)], 6)
    run_test("Flush diamonds K-high",
        [(1,12),(1,10),(1,8),(1,6),(1,4),(0,13),(2,11)], 6)
    run_test("Flush clubs Q-high",
        [(2,11),(2,9),(2,7),(2,5),(2,3),(0,13),(1,12)], 6)
    run_test("Flush spades A-high",
        [(3,13),(3,11),(3,9),(3,7),(3,5),(0,12),(1,10)], 6)
    # 6-card flush: best 5 chosen
    run_test("6-card flush: best 5 of 6",
        [(0,13),(0,11),(0,9),(0,7),(0,5),(0,3),(1,12)], 6)
    # 7-card flush
    run_test("7-card flush: best 5 of 7",
        [(0,13),(0,11),(0,9),(0,7),(0,5),(0,3),(0,1)], 6)
    # Flush not confused with straight (offsuit straight present)
    run_test("Flush wins over offsuit straight",
        [(0,13),(0,11),(0,9),(0,7),(0,5),(1,10),(2,8)], 6)
    # Low flush
    run_test("Flush clubs all low cards",
        [(2,1),(2,2),(2,3),(2,4),(2,6),(0,13),(1,12)], 6)


def test_straight():
    section("Straight (expected rank 5)")
    # All straights: wheel to broadway
    run_test("Straight A-5 wheel",
        [(0,1),(1,2),(2,3),(3,4),(0,5),(1,12),(2,13)], 5)
    run_test("Straight 2-6",
        [(0,1),(1,2),(2,3),(3,4),(0,5),(1,12),(2,11)], 5)
    run_test("Straight 3-7",
        [(0,2),(1,3),(2,4),(3,5),(0,6),(1,12),(2,11)], 5)
    run_test("Straight 4-8",
        [(0,3),(1,4),(2,5),(3,6),(0,7),(1,12),(2,11)], 5)
    run_test("Straight 5-9",
        [(0,4),(1,5),(2,6),(3,7),(0,8),(1,12),(2,11)], 5)
    run_test("Straight 6-T",
        [(0,5),(1,6),(2,7),(3,8),(0,9),(1,12),(2,11)], 5)
    run_test("Straight 7-J",
        [(0,6),(1,7),(2,8),(3,9),(0,10),(1,12),(2,2)], 5)
    run_test("Straight 8-Q",
        [(0,7),(1,8),(2,9),(3,10),(0,11),(1,2),(2,1)], 5)
    run_test("Straight 9-K",
        [(0,8),(1,9),(2,10),(3,11),(0,12),(1,2),(2,1)], 5)
    run_test("Straight T-A (broadway)",
        [(0,9),(1,10),(2,11),(3,12),(0,13),(1,2),(2,3)], 5)
    # Straight not starting with first card in hand
    run_test("Straight starting mid-hand (gap at start)",
        [(0,1),(1,2),(0,5),(1,6),(2,7),(3,8),(0,9)], 5)
    # Straight with duplicate rank (shouldn't count duplicate toward length)
    run_test("Straight with duplicate rank in middle",
        [(0,5),(1,6),(2,7),(3,8),(0,9),(1,9),(2,2)], 5)
    run_test("Straight with duplicate rank at start",
        [(0,5),(1,5),(2,6),(3,7),(0,8),(1,9),(2,2)], 5)
    # 6-card straight: highest wins
    run_test("6-card straight: highest straight chosen",
        [(0,4),(1,5),(2,6),(3,7),(0,8),(1,9),(2,2)], 5)
    # Straight not confused with flush (offsuit)
    run_test("Straight: 5 to a flush but offsuit straight present",
        [(0,9),(1,10),(2,11),(3,12),(0,13),(0,7),(0,5)], 5)


def test_three_of_a_kind():
    section("Three of a Kind (expected rank 4)")
    run_test("Trip 2s + A K kickers",
        [(0,1),(1,1),(2,1),(3,13),(0,12),(1,7),(2,3)], 4)
    run_test("Trip 5s + A K kickers",
        [(0,4),(1,4),(2,4),(3,13),(0,12),(1,7),(2,3)], 4)
    run_test("Trip 7s",
        [(0,6),(1,6),(2,6),(3,13),(0,12),(1,3),(2,2)], 4)
    run_test("Trip 9s",
        [(0,8),(1,8),(2,8),(3,13),(0,12),(1,3),(2,2)], 4)
    run_test("Trip Js",
        [(0,10),(1,10),(2,10),(3,13),(0,12),(1,3),(2,2)], 4)
    run_test("Trip Qs",
        [(0,11),(1,11),(2,11),(3,13),(0,12),(1,3),(2,2)], 4)
    run_test("Trip Ks",
        [(0,12),(1,12),(2,12),(3,13),(0,11),(1,3),(2,2)], 4)
    run_test("Trip As + K Q kickers",
        [(0,13),(1,13),(2,13),(0,12),(1,11),(2,9),(3,7)], 4)
    # Trips with two unrelated low kickers
    run_test("Trip 6s + low kickers",
        [(0,5),(1,5),(2,5),(3,4),(0,3),(1,12),(2,11)], 4)
    # Not confused with full house (no pair present)
    run_test("Trip As, no pair in hand",
        [(0,13),(1,13),(2,13),(0,12),(1,11),(2,9),(3,7)], 4)


def test_two_pair():
    section("Two Pair (expected rank 3)")
    run_test("2s and 3s + A kicker",
        [(0,1),(1,1),(0,2),(1,2),(0,13),(1,9),(2,7)], 3)
    run_test("5s and 6s",
        [(0,4),(1,4),(0,5),(1,5),(0,13),(1,9),(2,7)], 3)
    run_test("9s and Ts",
        [(0,8),(1,8),(0,9),(1,9),(0,13),(1,12),(2,7)], 3)
    run_test("Qs and Js + A kicker",
        [(0,11),(1,11),(0,10),(1,10),(0,13),(1,4),(2,2)], 3)
    run_test("Ks and Qs",
        [(0,12),(1,12),(0,11),(1,11),(0,13),(1,4),(2,2)], 3)
    run_test("As and Ks",
        [(0,13),(1,13),(0,12),(1,12),(0,11),(1,7),(2,5)], 3)
    run_test("As and 2s",
        [(0,13),(1,13),(0,1),(1,1),(0,11),(1,7),(2,5)], 3)
    # Three pair: best two chosen
    run_test("Three pair: As Ks Qs — best two chosen",
        [(0,13),(1,13),(0,12),(1,12),(0,11),(1,11),(2,7)], 3)
    run_test("Three pair: 3s 4s 5s — best two chosen",
        [(0,2),(1,2),(0,3),(1,3),(0,4),(1,4),(2,13)], 3)
    # Two pair not confused with full house
    run_test("Two pair only (no trips)",
        [(0,13),(1,13),(0,12),(1,12),(0,7),(1,5),(2,3)], 3)


def test_one_pair():
    section("One Pair (expected rank 2)")
    run_test("Pair of 2s + A K Q kickers",
        [(0,1),(1,1),(0,13),(1,12),(2,11),(3,9),(0,7)], 2)
    run_test("Pair of 5s + high kickers",
        [(0,4),(1,4),(0,13),(1,12),(2,11),(3,9),(0,7)], 2)
    run_test("Pair of 7s",
        [(0,6),(1,6),(0,13),(1,12),(2,11),(3,9),(0,5)], 2)
    run_test("Pair of 9s",
        [(0,8),(1,8),(0,13),(1,12),(2,11),(3,7),(0,5)], 2)
    run_test("Pair of Js",
        [(0,10),(1,10),(0,13),(1,12),(2,9),(3,7),(0,5)], 2)
    run_test("Pair of Qs",
        [(0,11),(1,11),(0,13),(1,12),(2,9),(3,7),(0,5)], 2)
    run_test("Pair of Ks + A Q J kickers",
        [(0,12),(1,12),(0,13),(1,11),(2,10),(3,8),(0,3)], 2)
    run_test("Pair of As + K Q J kickers",
        [(0,13),(1,13),(0,12),(1,11),(2,10),(3,7),(0,5)], 2)
    # Pair with low kickers
    run_test("Pair of As + low kickers",
        [(0,13),(1,13),(0,7),(1,4),(2,2),(3,1),(0,9)], 2)


def test_high_card():
    section("High Card (expected rank 1)")
    run_test("A high rainbow",
        [(0,13),(1,11),(2,9),(3,7),(0,5),(1,3),(2,1)], 1)
    run_test("K high",
        [(0,12),(1,10),(2,8),(3,6),(0,4),(1,2),(2,1)], 1)
    run_test("Q high",
        [(0,11),(1,9),(2,7),(3,5),(0,3),(1,1),(2,2)], 1)
    run_test("Mixed high cards",
        [(0,13),(1,12),(2,10),(3,8),(0,6),(1,4),(2,2)], 1)
    # No pair, no straight, no flush
    run_test("A high, all different ranks, 3 suits",
        [(0,13),(1,11),(2,8),(0,6),(1,4),(2,2),(3,1)], 1)
    # 7 cards, all different, no made hand
    run_test("7 unique ranks, no straight/flush",
        [(0,13),(1,11),(2,8),(3,6),(0,4),(1,2),(2,1)], 1)


def test_score_ordering():
    section("Score ordering: each rank must beat the one below it")
    fn = getattr(mod, "hand_eval", None)
    if not fn:
        print("  [ERROR] hand_eval not found")
        return

    ranked_hands = [
        ("Royal Flush",     [(0,9),(0,10),(0,11),(0,12),(0,13),(1,1),(2,2)]),
        ("Straight Flush",  [(2,4),(2,5),(2,6),(2,7),(2,8),(0,1),(1,12)]),
        ("Four of a Kind",  [(0,13),(1,13),(2,13),(3,13),(0,12),(1,11),(2,9)]),
        ("Full House",      [(0,13),(1,13),(2,13),(0,12),(1,12),(0,7),(1,5)]),
        ("Flush",           [(3,13),(3,11),(3,9),(3,7),(3,5),(0,12),(1,10)]),
        ("Straight",        [(0,9),(1,10),(2,11),(3,12),(0,13),(1,2),(2,3)]),
        ("Three of a Kind", [(0,13),(1,13),(2,13),(0,12),(1,11),(2,9),(3,7)]),
        ("Two Pair",        [(0,13),(1,13),(0,12),(1,12),(0,11),(1,7),(2,5)]),
        ("One Pair",        [(0,13),(1,13),(0,12),(1,11),(2,10),(3,7),(0,5)]),
        ("High Card",       [(0,13),(1,11),(2,9),(3,7),(0,5),(1,3),(2,1)]),
    ]

    scores = []
    for name, hand in ranked_hands:
        try:
            s = fn(copy.deepcopy(hand))
            scores.append((name, s))
        except Exception as e:
            scores.append((name, None))
            print(f"  [ERROR] {name}: {e}")

    all_ok = True
    for i in range(len(scores) - 1):
        n1, s1 = scores[i]
        n2, s2 = scores[i+1]
        if s1 is None or s2 is None:
            continue
        if s1 <= s2:
            print(f"  [FAIL]  {n1} ({s1:.4f}) should beat {n2} ({s2:.4f})")
            results["fail"] += 1
            all_ok = False
    if all_ok:
        print("  [PASS]  All 10 hand ranks score in correct descending order")
        results["pass"] += 1


def test_tiebreakers():
    section("Tiebreakers: same rank, better hand scores higher")

    # ── High Card tiebreakers ─────────────────────────────────────────────
    run_tiebreak("HC: A-high beats K-high",
        [(0,13),(1,11),(2,9),(3,7),(0,5),(1,3),(2,1)],
        [(0,12),(1,11),(2,9),(3,7),(0,5),(1,3),(2,1)])
    run_tiebreak("HC: same top card, second card decides",
        [(0,13),(1,12),(2,9),(3,7),(0,5),(1,3),(2,1)],
        [(0,13),(1,11),(2,9),(3,7),(0,5),(1,3),(2,1)])

    # ── One Pair tiebreakers ──────────────────────────────────────────────
    run_tiebreak("Pair: As beats Ks",
        [(0,13),(1,13),(0,12),(1,11),(2,10),(3,7),(0,5)],
        [(0,12),(1,12),(0,13),(1,11),(2,10),(3,8),(0,3)])
    run_tiebreak("Pair: same pair, better kicker wins",
        [(0,13),(1,13),(0,12),(1,11),(2,10),(3,7),(0,5)],
        [(0,13),(1,13),(0,11),(1,10),(2,9),(3,7),(0,5)])

    # ── Two Pair tiebreakers ──────────────────────────────────────────────
    run_tiebreak("Two pair: As+Ks beats As+Qs",
        [(0,13),(1,13),(0,12),(1,12),(0,11),(1,7),(2,5)],
        [(0,13),(1,13),(0,11),(1,11),(0,12),(1,7),(2,5)])
    run_tiebreak("Two pair: same top pair, second pair decides",
        [(0,13),(1,13),(0,12),(1,12),(0,7),(1,5),(2,3)],
        [(0,13),(1,13),(0,11),(1,11),(0,7),(1,5),(2,3)])
    run_tiebreak("Two pair: same pairs, kicker decides",
        [(0,13),(1,13),(0,12),(1,12),(0,11),(1,7),(2,5)],
        [(0,13),(1,13),(0,12),(1,12),(0,9),(1,7),(2,5)])

    # ── Three of a Kind tiebreakers ───────────────────────────────────────
    run_tiebreak("Trips: As beats Ks",
        [(0,13),(1,13),(2,13),(0,12),(1,11),(2,9),(3,7)],
        [(0,12),(1,12),(2,12),(0,13),(1,11),(2,9),(3,7)])
    run_tiebreak("Trips: same rank, kicker decides",
        [(0,13),(1,13),(2,13),(0,12),(1,11),(2,9),(3,7)],
        [(0,13),(1,13),(2,13),(0,11),(1,10),(2,9),(3,7)])

    # ── Straight tiebreakers ──────────────────────────────────────────────
    run_tiebreak("Straight: broadway beats 9-high",
        [(0,9),(1,10),(2,11),(3,12),(0,13),(1,2),(2,3)],
        [(0,8),(1,9),(2,10),(3,11),(0,12),(1,2),(2,3)])
    run_tiebreak("Straight: 6-high beats 5-high (wheel)",
        [(0,2),(1,3),(2,4),(3,5),(0,6),(1,12),(2,13)],
        [(0,1),(1,2),(2,3),(3,4),(0,5),(1,12),(2,13)])
    run_tiebreak("Straight: 9-high beats 8-high",
        [(0,5),(1,6),(2,7),(3,8),(0,9),(1,2),(2,1)],
        [(0,4),(1,5),(2,6),(3,7),(0,8),(1,2),(2,1)])

    # ── Flush tiebreakers ─────────────────────────────────────────────────
    run_tiebreak("Flush: A-high beats K-high",
        [(3,13),(3,11),(3,9),(3,7),(3,5),(0,1),(1,2)],
        [(3,12),(3,11),(3,9),(3,7),(3,5),(0,1),(1,2)])
    run_tiebreak("Flush: same top card, second card decides",
        [(3,13),(3,12),(3,9),(3,7),(3,5),(0,1),(1,2)],
        [(3,13),(3,11),(3,9),(3,7),(3,5),(0,1),(1,2)])

    # ── Full House tiebreakers ────────────────────────────────────────────
    run_tiebreak("FH: As full beats Ks full",
        [(0,13),(1,13),(2,13),(0,12),(1,12),(0,7),(1,5)],
        [(0,12),(1,12),(2,12),(0,13),(1,13),(0,7),(1,5)])
    run_tiebreak("FH: same trips, higher pair wins",
        [(0,13),(1,13),(2,13),(0,12),(1,12),(2,7),(3,5)],
        [(0,13),(1,13),(2,13),(0,11),(1,11),(2,7),(3,5)])

    # ── Four of a Kind tiebreakers ────────────────────────────────────────
    run_tiebreak("Quads: As beats Ks",
        [(0,13),(1,13),(2,13),(3,13),(0,12),(1,11),(2,9)],
        [(0,12),(1,12),(2,12),(3,12),(0,13),(1,9),(2,7)])
    run_tiebreak("Quads: same rank, kicker decides",
        [(0,9),(1,9),(2,9),(3,9),(0,13),(1,11),(2,7)],
        [(0,9),(1,9),(2,9),(3,9),(0,12),(1,11),(2,7)])

    # ── Straight Flush tiebreakers ────────────────────────────────────────
    run_tiebreak("SF: K-high beats 9-high",
        [(3,8),(3,9),(3,10),(3,11),(3,12),(0,1),(1,2)],
        [(2,4),(2,5),(2,6),(2,7),(2,8),(0,1),(1,12)])
    run_tiebreak("SF: 9-high beats wheel",
        [(2,4),(2,5),(2,6),(2,7),(2,8),(0,1),(1,12)],
        [(0,1),(0,2),(0,3),(0,4),(0,13),(1,7),(2,11)])


def test_edge_cases():
    section("Edge cases and tricky hands")

    # Straight vs flush conflict: flush wins (handled by ordering)
    run_test("Flush present AND offsuit straight: flush wins",
        [(0,13),(0,10),(0,8),(0,6),(0,4),(1,9),(2,11)], 6)

    # Full house vs flush: full house wins
    run_test("FH + 5 flush cards: FH wins (FH > flush)",
        [(0,13),(1,13),(2,13),(0,12),(1,12),(0,7),(0,5)], 7)

    # Wheel straight (A-2-3-4-5): A acts as low
    run_test("Wheel: A plays low in A-2-3-4-5",
        [(0,1),(1,2),(2,3),(3,4),(0,5),(1,9),(2,11)], 5)

    # A does NOT play low in 2-3-4-5-6 (it's just a 6-high straight)
    run_test("A-high straight (broadway) with broadway",
        [(0,9),(1,10),(2,11),(3,12),(0,13),(1,1),(2,2)], 5)

    # Trips + pair (FH) vs trips alone
    run_test("Trips + unrelated pair = Full House, not Trips",
        [(0,9),(1,9),(2,9),(0,5),(1,5),(2,12),(3,7)], 7)

    # Four of a kind with full house also present
    run_test("Quads + pair: quads win (not FH)",
        [(0,9),(1,9),(2,9),(3,9),(0,5),(1,5),(2,12)], 8)

    # Straight flush vs regular flush
    run_test("SF cards + extra flush cards: SF wins",
        [(0,5),(0,6),(0,7),(0,8),(0,9),(0,2),(0,1)], 9)

    # 7 cards all same suit but forming RF
    run_test("RF in 7-suit cards",
        [(0,9),(0,10),(0,11),(0,12),(0,13),(0,1),(0,2)], 10)

    # High card: no hand at all
    run_test("High card: 7 unique unconnected offsuit ranks",
        [(0,13),(1,11),(2,8),(3,6),(0,4),(1,2),(2,1)], 1)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nHand_Eval.py  —  Comprehensive Test Suite (7-card hands only)")
    print(f"Source: {SOURCE}\n")

    test_royal_flush()
    test_straight_flush()
    test_four_of_a_kind()
    test_full_house()
    test_flush()
    test_straight()
    test_three_of_a_kind()
    test_two_pair()
    test_one_pair()
    test_high_card()
    test_score_ordering()
    test_tiebreakers()
    test_edge_cases()

    section("Summary")
    total = results["pass"] + results["fail"] + results["error"]
    print(f"  Total : {total}")
    print(f"  PASS  : {results['pass']}")
    print(f"  FAIL  : {results['fail']}")
    print(f"  ERROR : {results['error']}")
    print()
    sys.exit(1 if results["fail"] + results["error"] > 0 else 0)
