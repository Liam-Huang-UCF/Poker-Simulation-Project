import random
from collections import Counter

# Define ranks and suits
ranks = "23456789TJQKA"
suits = "shdc"

# Helper functions
def card_rank_value(card):
    return ranks.index(card[0])

def is_connector(card1, card2):
    return abs(card_rank_value(card1) - card_rank_value(card2)) == 1

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

def hand_strength(hand, board):
    all_cards = hand + board
    return max(card_rank_value(card) for card in all_cards)

def pretty_hand(hand):
    return ' '.join(hand)

def simulate_one_round():
    # Setup deck and players
    deck = [r + s for r in ranks for s in suits]
    random.shuffle(deck)
    players = [deck[i*2:(i+1)*2] for i in range(5)]
    remaining_deck = deck[10:]
    board = remaining_deck[:5]

    print("\n=== Poker Round Simulation ===\n")

    # Display each player's hand and whether they fold
    active_players = []
    for idx, hand in enumerate(players):
        folds = should_fold(hand)
        print(f"Player {idx + 1}: {pretty_hand(hand)} {'(FOLDS)' if folds else '(PLAYS)'}")
        if not folds:
            active_players.append((idx, hand))

    print("\nTable Cards:", pretty_hand(board))

    if len(active_players) < 2:
        print("\nNot enough players to continue the hand (everyone folded).")
        return

    # Determine the winner
    strengths = [(idx, hand_strength(hand, board)) for idx, hand in active_players]
    max_strength = max(score for _, score in strengths)
    winners = [idx for idx, score in strengths if score == max_strength]

    print("\nResults:")
    if len(winners) == 1:
        print(f"Player {winners[0] + 1} wins the hand!")
    else:
        print("It's a tie between:", ', '.join(f"Player {w+1}" for w in winners))

# Run one simulation
if __name__ == "__main__":
    simulate_one_round()
