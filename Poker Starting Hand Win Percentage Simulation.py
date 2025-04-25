import random
from collections import Counter, defaultdict
from typing import List, Tuple

ranks = "23456789TJQKA"
suits = "shdc"

def card_rank_value(card):
    return ranks.index(card[0])

def is_connector(card1, card2):
    return abs(card_rank_value(card1) - card_rank_value(card2)) == 1

def hand_type(hand: List[str]) -> str:
    r1, s1 = hand[0][0], hand[0][1]
    r2, s2 = hand[1][0], hand[1][1]
    val1, val2 = card_rank_value(hand[0]), card_rank_value(hand[1])
    
    if r1 == r2:
        return "Pocket Pair"
    elif s1 == s2:
        return "Suited Connector" if is_connector(hand[0], hand[1]) else "Suited Non-Connector"
    else:
        return "Offsuit Connector" if is_connector(hand[0], hand[1]) else "Offsuit Non-Connector"

def should_fold(hand):
    r1, r2 = hand[0][0], hand[1][0]
    idx1, idx2 = ranks.index(r1), ranks.index(r2)
    
    ranks_numeric = {r: i for i, r in enumerate(ranks)}  # map for quick lookup
    val1, val2 = ranks_numeric[r1], ranks_numeric[r2]

    # Rule 1: When both cards ≤6, fold unless pair or A+x
    if val1 <= 4 and val2 <= 4:
        if r1 == r2 or r1 == 'A' or r2 == 'A':
            return False
        return True
    
    # Rule 2: Hands with a 7
    if r1 == '7' or r2 == '7':
        good_combos = [('7', '7'), ('7', 'A'), ('7', '8')]
        if (r1, r2) not in good_combos and (r2, r1) not in good_combos:
            return True
    
    # Rule 3: Hands with an 8
    if r1 == '8' or r2 == '8':
        good_combos = [('8', '8'), ('8', 'A'), ('8', '7'), ('8', '9'), ('8', 'T')]
        if (r1, r2) not in good_combos and (r2, r1) not in good_combos:
            return True

    # Rule 4: 9 with a small card (≤7)
    if r1 == '9' and val2 <= 5:
        return True
    if r2 == '9' and val1 <= 5:
        return True

    return False  # otherwise play it

def hand_strength(hand: List[str], board: List[str]) -> int:
    all_cards = hand + board
    return max(card_rank_value(card) for card in all_cards)

def simulate_hand_type_wins(num_simulations: int = 10000) -> dict:
    win_counts = defaultdict(int)
    play_counts = defaultdict(int)
    total_games = 0

    for sim in range(1, num_simulations + 1):
        deck = [r + s for r in ranks for s in suits]
        random.shuffle(deck)
        hands = [deck[i*2:(i+1)*2] for i in range(5)]
        remaining_deck = deck[10:]
        board = remaining_deck[:5]

        active_players = []
        for i, hand in enumerate(hands):
            if not should_fold(hand):
                htype = hand_type(hand)
                active_players.append((htype, hand))

        if len(active_players) < 2:
            continue

        scores = [(htype, hand_strength(hand, board)) for htype, hand in active_players]
        max_score = max(score for _, score in scores)
        winners = [htype for htype, score in scores if score == max_score]

        for htype in set(htype for htype, _ in active_players):
            play_counts[htype] += 1

        for htype in winners:
            win_counts[htype] += 1 / winners.count(htype)

        total_games += 1

        # Print every 1000 simulations
        if sim % 1000 == 0:
            print(f"\nAfter {sim} simulations:")
            temp_win_rates = {
                htype: round((win_counts[htype] / play_counts[htype]) * 100, 2)
                for htype in play_counts if play_counts[htype] > 0
            }
            for htype, rate in temp_win_rates.items():
                print(f"{htype}: {rate}%")

    # Final results
    win_rates = {
        htype: round((win_counts[htype] / play_counts[htype]) * 100, 2)
        for htype in play_counts if play_counts[htype] > 0
    }

    return win_rates

if __name__ == "__main__":
    results = simulate_hand_type_wins(10000)
    print("\nFinal Win Rates by Hand Type (out of 10,000 games):")
    for htype, rate in results.items():
        print(f"{htype}: {rate}%")

    input("\nPress Enter to exit...")