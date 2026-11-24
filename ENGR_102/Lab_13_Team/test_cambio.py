"""
test_cambio.py - Our ten test cases.

Run:  python -m unittest test_cambio -v
These only test the rules (cambio_logic.py), so no window opens.
"""

import random
import unittest

from cambio_logic import (
    CambioGame, Card, calculate_scores, cards_in, check_action_card, create_deck,
    deal_cards, determine_winner, get_card_value, shuffle_deck, valid_player_count,
)


def rigged_game(num_players, hands, first_player=0):
    """A game where we choose exactly which cards everyone holds."""
    game = CambioGame(num_players, rng=random.Random(1), first_player=first_player)
    game.hands = [list(h) for h in hands]
    return game


class TestCambio(unittest.TestCase):

    # 1
    def test_player_count(self):
        self.assertEqual(valid_player_count("2"), 2)
        self.assertEqual(valid_player_count("6"), 6)
        for bad in ("1", "7", "0", "-3", "abc", "", "2.5"):
            self.assertIsNone(valid_player_count(bad), bad)

    # 2
    def test_deck_creation_and_shuffle(self):
        deck = create_deck()
        self.assertEqual(len(deck), 54)
        names = {str(c) for c in deck}
        self.assertEqual(len(names), 54)  # no duplicates
        before = list(deck)
        shuffle_deck(deck, random.Random(42))
        self.assertEqual(len(deck), 54)
        self.assertEqual(set(map(id, before)), set(map(id, deck)))  # same cards
        self.assertNotEqual([id(c) for c in before], [id(c) for c in deck])  # new order

    # 3
    def test_dealing(self):
        deck = create_deck()
        hands = deal_cards(deck, 4)
        self.assertTrue(all(len(h) == 4 for h in hands))
        self.assertEqual(len(deck), 38)

    # 4
    def test_card_values(self):
        self.assertEqual(get_card_value(Card("JOKER", "R")), 0)
        self.assertEqual(get_card_value(Card("A", "S")), 1)
        self.assertEqual(get_card_value(Card("7", "D")), 7)
        self.assertEqual(get_card_value(Card("J", "C")), 10)
        self.assertEqual(get_card_value(Card("Q", "H")), 10)
        self.assertEqual(get_card_value(Card("K", "S")), 10)   # black king
        self.assertEqual(get_card_value(Card("K", "H")), -1)   # red king

    # 5
    def test_action_cards(self):
        self.assertEqual(check_action_card(Card("7", "S")), "peek_own")
        self.assertEqual(check_action_card(Card("8", "H")), "peek_own")
        self.assertEqual(check_action_card(Card("9", "D")), "peek_opp")
        self.assertEqual(check_action_card(Card("10", "C")), "peek_opp")
        self.assertEqual(check_action_card(Card("J", "S")), "blind_swap")
        self.assertEqual(check_action_card(Card("Q", "H")), "blind_swap")
        self.assertEqual(check_action_card(Card("K", "C")), "look_swap")
        for rank, suit in (("2", "S"), ("6", "H"), ("A", "D"), ("JOKER", "B"), ("K", "D")):
            self.assertIsNone(check_action_card(Card(rank, suit)), rank + suit)

    # 6
    def test_replace_card(self):
        game = CambioGame(2, rng=random.Random(3))
        p = game.current_player
        old = game.hands[p][1]
        drawn = game.draw_card()
        game.replace_card(p, 1, drawn)
        self.assertIs(game.hands[p][1], drawn)
        self.assertIs(game.top_discard(), old)
        self.assertEqual(game.hand_size(p), 4)

    # 7
    def test_correct_stick(self):
        five = Card("5", "S")
        game = rigged_game(2, [[Card("2", "H"), five, Card("9", "C"), Card("K", "D")],
                               [Card("3", "H"), Card("4", "H"), Card("6", "H"), Card("Q", "H")]])
        game.discard(Card("5", "D"))
        deck_before = len(game.deck)
        self.assertEqual(game.stick_card(0, 0, 1), "match")
        self.assertEqual(game.hand_size(0), 3)
        self.assertIs(game.top_discard(), five)
        self.assertEqual(len(game.deck), deck_before)  # no penalty card drawn

    # 8
    def test_wrong_stick_penalty(self):
        game = rigged_game(2, [[Card("2", "H"), Card("8", "S"), Card("9", "C"), Card("K", "D")],
                               [Card("3", "H"), Card("4", "H"), Card("6", "H"), Card("Q", "H")]])
        game.discard(Card("5", "D"))
        self.assertEqual(game.stick_card(0, 0, 1), "miss")
        self.assertEqual(game.hand_size(0), 5)
        self.assertEqual(game.hands[0][1].rank, "8")  # card went back where it was

    # 9
    def test_double_stick(self):
        game = rigged_game(2, [[Card("5", "S"), Card("2", "S"), Card("3", "S"), Card("4", "S")],
                               [Card("5", "C"), Card("2", "C"), Card("3", "C"), Card("4", "C")]])
        game.discard(Card("5", "D"))
        self.assertEqual(game.stick_card(0, 0, 0), "match")       # first player is right
        self.assertEqual(game.stick_card(1, 1, 0), "late")        # second is too late
        self.assertEqual(game.hand_size(0), 3)
        self.assertEqual(game.hand_size(1), 5)

    # 10
    def test_cambio_and_scoring(self):
        game = CambioGame(3, rng=random.Random(5), first_player=0)
        game.call_cambio(0)
        self.assertFalse(game.end_turn())         # player 0 called
        self.assertEqual(game.current_player, 1)
        with self.assertRaises(ValueError):       # caller's cards are locked
            game.blind_swap(1, 0, 0, 0)
        game.discard(game.draw_card())
        self.assertEqual(game.stick_card(1, 0, 0), "locked")  # can't stick them either
        self.assertFalse(game.end_turn())         # player 1's last turn
        self.assertEqual(game.current_player, 2)
        self.assertTrue(game.end_turn())          # player 2's last turn -> game over

        hand = [Card("JOKER", "R"), Card("A", "S"), Card("K", "H"), Card("3", "D")]
        scores = calculate_scores([hand, [Card("4", "S")], [Card("3", "C")]])
        self.assertEqual(scores, [3, 4, 3])
        self.assertEqual(determine_winner(scores), [0, 2])  # a tie: both win


class TestExtras(unittest.TestCase):
    def test_stick_opponent_and_give(self):
        target = Card("9", "H")
        game = rigged_game(2, [[Card("2", "H"), Card("3", "S"), Card("4", "C"), Card("6", "D")],
                               [Card("A", "H"), target, Card("7", "H"), Card("Q", "H")]])
        game.discard(Card("9", "S"))
        self.assertEqual(game.stick_card(0, 1, 1), "match_opponent")
        self.assertIsNone(game.hands[1][1])
        gift = game.give_card(0, 0, 1, 1)
        self.assertIs(game.hands[1][1], gift)       # the gift fills the empty slot
        self.assertEqual(game.hand_size(0), 3)
        self.assertEqual(game.hand_size(1), 4)

    def test_deck_reshuffles_when_empty(self):
        game = CambioGame(2, rng=random.Random(9))
        while game.deck:
            game.discard(game.deck.pop())
        top = game.top_discard()
        card = game.draw_card()
        self.assertIsNotNone(card)
        self.assertEqual(game.discard_pile, [top])

    def test_total_cards_never_change(self):
        """Play 300 random games and make sure no card is ever lost or copied."""
        for seed in range(300):
            rng = random.Random(seed)
            game = CambioGame(rng.randint(2, 6), rng=rng)
            for _ in range(200):
                if game.over:
                    break
                p = game.current_player
                if rng.random() < 0.03 and game.can_call_cambio():
                    game.call_cambio(p)
                else:
                    card = game.draw_card()
                    if card is None:  # every card is in someone's hand: the game ends
                        break
                    slots = [i for i, c in enumerate(game.hands[p]) if c is not None]
                    if slots and rng.random() < 0.5:
                        game.replace_card(p, rng.choice(slots), card)
                    else:
                        game.discard(card)
                    s = rng.randrange(game.num_players)
                    o = rng.randrange(game.num_players)
                    o_slots = [i for i, c in enumerate(game.hands[o]) if c is not None]
                    if o_slots:
                        game.stick_card(s, o, rng.choice(o_slots))
                game.end_turn()
                total = len(game.deck) + len(game.discard_pile) + sum(len(cards_in(h)) for h in game.hands)
                self.assertEqual(total, 54)


if __name__ == "__main__":
    unittest.main(verbosity=2)
