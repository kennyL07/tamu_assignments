"""
cambio_logic.py - The rules of Cambio, with no graphics.

The function names match the boxes in our hierarchy chart. Keeping the rules
separate from the PyGame code (cambio.py) means we can test them without
opening a window (see test_cambio.py).

A player's hand is a list of "slots". When a card is stuck (discarded out of
a hand), its slot becomes None so the other cards don't move around. That
matters because remembering WHERE your cards are is the whole game.
"""

import random
from dataclasses import dataclass

MIN_PLAYERS = 2
MAX_PLAYERS = 6
HAND_SIZE = 4

SUITS = ("S", "H", "D", "C")
SUIT_NAMES = {"S": "spades", "H": "hearts", "D": "diamonds", "C": "clubs"}
RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
RANK_NAMES = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King", "JOKER": "Joker"}

ACTION_DESCRIPTIONS = {
    "peek_own": "Peek at one of your cards",
    "peek_opp": "Peek at someone else's card",
    "blind_swap": "Blind swap with someone",
    "look_swap": "Look at 2 cards, then swap",
}


@dataclass(eq=False)  # eq=False: every card is its own object, even two jokers
class Card:
    rank: str  # "A", "2".."10", "J", "Q", "K" or "JOKER"
    suit: str  # "S", "H", "D", "C"; jokers use "R" (red) or "B" (black)

    @property
    def is_red(self):
        return self.suit in ("H", "D", "R")

    @property
    def is_joker(self):
        return self.rank == "JOKER"

    def __str__(self):
        if self.is_joker:
            return ("red" if self.is_red else "black") + " Joker"
        name = RANK_NAMES.get(self.rank, self.rank)
        return f"{name} of {SUIT_NAMES[self.suit]}"


# ---------------------------------------------------------------- setup

def valid_player_count(text):
    """Check the typed player count. Returns the number, or None if invalid."""
    try:
        n = int(str(text).strip())
    except ValueError:
        return None
    return n if MIN_PLAYERS <= n <= MAX_PLAYERS else None


def player_order(num_players, first=None, rng=random):
    """Turn order: start from `first` (random if not given) and go around the table."""
    if first is None:
        first = rng.randrange(num_players)
    return [(first + i) % num_players for i in range(num_players)]


def create_deck():
    """52 standard cards plus a red and a black joker (54 total)."""
    deck = [Card(rank, suit) for suit in SUITS for rank in RANKS]
    deck += [Card("JOKER", "R"), Card("JOKER", "B")]
    return deck


def shuffle_deck(deck, rng=random):
    rng.shuffle(deck)
    return deck


def deal_cards(deck, num_players, hand_size=HAND_SIZE):
    """Deal `hand_size` cards to each player, one at a time around the table."""
    hands = [[] for _ in range(num_players)]
    for _ in range(hand_size):
        for hand in hands:
            hand.append(deck.pop())
    return hands


# ---------------------------------------------------------------- card rules

def get_card_value(card):
    """Joker 0, Ace 1, numbers face value, J/Q 10, black King 10, red King -1."""
    if card.is_joker:
        return 0
    if card.rank == "A":
        return 1
    if card.rank == "K":
        return -1 if card.is_red else 10
    if card.rank in ("J", "Q"):
        return 10
    return int(card.rank)


def check_action_card(card):
    """Return the action a discarded card gives, or None."""
    if card.rank in ("7", "8"):
        return "peek_own"
    if card.rank in ("9", "10"):
        return "peek_opp"
    if card.rank in ("J", "Q"):
        return "blind_swap"
    if card.rank == "K" and not card.is_red:
        return "look_swap"
    return None


def check_match(card_a, card_b):
    """Sticking only needs the same number / face (suit doesn't matter)."""
    return card_a is not None and card_b is not None and card_a.rank == card_b.rank


def cards_in(hand):
    return [c for c in hand if c is not None]


def calculate_scores(hands):
    return [sum(get_card_value(c) for c in cards_in(hand)) for hand in hands]


def determine_winner(scores):
    """Everyone tied for the lowest score wins (a list of player numbers)."""
    lowest = min(scores)
    return [p for p, s in enumerate(scores) if s == lowest]


# ---------------------------------------------------------------- the game

class CambioGame:
    def __init__(self, num_players, rng=None, first_player=None):
        if valid_player_count(num_players) is None:
            raise ValueError(f"Cambio needs {MIN_PLAYERS}-{MAX_PLAYERS} players")
        self.rng = rng or random.Random()
        self.num_players = num_players
        self.order = player_order(num_players, first_player, self.rng)
        self.turn_index = 0
        self.deck = shuffle_deck(create_deck(), self.rng)
        self.hands = deal_cards(self.deck, num_players)
        self.discard_pile = []
        self.discard_claimed = False  # True once someone has stuck on the top discard
        self.cambio_caller = None
        self.final_turns_left = 0
        self.over = False
        self.log = []

    # ---- helpers
    def log_event(self, message):
        self.log.append(message)

    @property
    def current_player(self):
        return self.order[self.turn_index]

    def top_discard(self):
        return self.discard_pile[-1] if self.discard_pile else None

    def hand_size(self, player):
        return len(cards_in(self.hands[player]))

    def opponents(self, player):
        return [p for p in range(self.num_players) if p != player]

    def is_locked(self, player):
        """The player who called Cambio has locked cards: nobody can touch them."""
        return self.cambio_caller is not None and player == self.cambio_caller

    def _trim(self, player):
        hand = self.hands[player]
        while hand and hand[-1] is None:
            hand.pop()

    # ---- drawing and discarding
    def _refill_deck(self):
        """If the deck runs out, shuffle the discard pile (except its top card) back in."""
        if self.deck or len(self.discard_pile) < 2:
            return
        top = self.discard_pile.pop()
        self.deck = shuffle_deck(self.discard_pile, self.rng)
        self.discard_pile = [top]
        self.log_event("The deck ran out, so the discard pile was shuffled into a new deck.")

    def draw_card(self):
        self._refill_deck()
        return self.deck.pop() if self.deck else None

    def discard(self, card):
        self.discard_pile.append(card)
        self.discard_claimed = False  # a fresh card can be stuck on

    def replace_card(self, player, index, new_card):
        """Put the drawn card into the hand; the old card goes to the discard pile."""
        old = self.hands[player][index]
        if old is None:
            raise ValueError("That slot is empty")
        self.hands[player][index] = new_card
        self.discard(old)
        return old

    # ---- action cards
    def swap_cards(self, player_a, index_a, player_b, index_b):
        if self.is_locked(player_a) or self.is_locked(player_b):
            raise ValueError("Those cards are locked (that player called Cambio)")
        hand_a, hand_b = self.hands[player_a], self.hands[player_b]
        if hand_a[index_a] is None or hand_b[index_b] is None:
            raise ValueError("Can't swap an empty slot")
        hand_a[index_a], hand_b[index_b] = hand_b[index_b], hand_a[index_a]

    def blind_swap(self, player_a, index_a, player_b, index_b):
        self.swap_cards(player_a, index_a, player_b, index_b)

    def look_swap(self, player_a, index_a, player_b, index_b):
        # Looking happens on screen; the swap itself is the same as a blind swap.
        self.swap_cards(player_a, index_a, player_b, index_b)

    # ---- sticking
    def penalty(self, player):
        """Wrong or late stick: the player gets one extra face-down card."""
        card = self.draw_card()
        if card is not None:
            self.hands[player].append(card)
        return card

    def claim_stick(self, sticker):
        """A player shouts "stick!". Returns 'ok', 'late', 'locked' or 'nothing'.
        If someone already stuck on this discard, the late player gets a penalty."""
        if self.top_discard() is None or self.over:
            return "nothing"
        if self.is_locked(sticker):
            return "locked"
        if self.discard_claimed:
            self.penalty(sticker)
            return "late"
        return "ok"

    def stick_card(self, sticker, owner, index):
        """`sticker` flips over `owner`'s card at `index`.
        Returns 'match', 'match_opponent', 'miss', 'late', 'locked' or 'nothing'."""
        claim = self.claim_stick(sticker)
        if claim != "ok":
            return claim
        if self.is_locked(owner):
            return "locked"
        card = self.hands[owner][index]
        if card is None:
            return "nothing"
        if check_match(card, self.top_discard()):
            self.hands[owner][index] = None
            self._trim(owner)
            self.discard_pile.append(card)
            self.discard_claimed = True
            return "match" if owner == sticker else "match_opponent"
        self.penalty(sticker)  # the card goes back where it was
        return "miss"

    def give_card(self, giver, index, receiver, position=None):
        """After sticking someone else's card, the sticker gives them one of
        their own cards (blind), into the empty slot if possible."""
        card = self.hands[giver][index]
        if card is None:
            raise ValueError("That slot is empty")
        self.hands[giver][index] = None
        self._trim(giver)
        hand = self.hands[receiver]
        if position is not None and position < len(hand) and hand[position] is None:
            hand[position] = card
        else:
            hand.append(card)
        return card

    # ---- turns and end of game
    def can_call_cambio(self):
        return self.cambio_caller is None and not self.over

    def call_cambio(self, player):
        if not self.can_call_cambio():
            raise ValueError("Cambio has already been called")
        self.cambio_caller = player
        self.final_turns_left = self.num_players - 1

    def end_turn(self):
        """Move to the next player. Returns True when the game is over."""
        if self.cambio_caller is not None and self.current_player != self.cambio_caller:
            self.final_turns_left -= 1
        if self.cambio_caller is not None and self.final_turns_left <= 0:
            self.over = True
            return True
        self.turn_index = (self.turn_index + 1) % self.num_players
        return False

    def scores(self):
        return calculate_scores(self.hands)

    def winners(self):
        return determine_winner(self.scores())
