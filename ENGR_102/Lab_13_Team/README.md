# Cambio (PyGame)

A hot-seat version of Cambio: 2–6 players share one screen and take turns.

## Run it

```
pip install pygame
python cambio.py
```

Run the ten test cases (no window opens):

```
python -m unittest test_cambio -v
```

Keep all three `.py` files in the same folder.

## Files

| File | What it does |
|---|---|
| `cambio_logic.py` | The rules only: deck, dealing, card values, action cards, sticking, penalties, Cambio, scoring |
| `cambio.py` | The PyGame window: table, cards, buttons, pass-the-device screens, rules overlay, confetti and KABOOM |
| `test_cambio.py` | Our 10 test cases, plus 3 extra checks |

## Controls

- **Click** your cards and the buttons in the right-hand panel.
- **R** shows or hides the rules.
- **1–6** after any discard: that player calls "stick", then clicks the card they think matches.
- **Space** or click to continue on a "Pass to Player X" screen.

## Secret ending: flip the table

Press **SPACE 10 times within 2 seconds** at any point during a game. Whoever is playing at that moment flips the table: the table tumbles over and every card flies off. The game ends with "Player X flipped the table. Nobody wins." and a **Play again** button.

- The settings are at the top of `cambio.py`: `FLIP_PRESSES`, `FLIP_WINDOW`, `FLIP_ANIM` and `GRAVITY`.
- The code is in `register_space()`, `flip_table()`, `draw_flip()` and `draw_flip_results()`.
- SPACE still works as normal on the "Pass to Player X" screen. Only fast mashing counts toward a flip.
- It doesn't work on the start screen or after the game is over.

## How the hierarchy chart maps to the code

| Chart box | Code |
|---|---|
| `player_count()` | `CambioApp.player_count()`, which uses `valid_player_count()` |
| `initialize_game()` | `CambioApp.initialize_game()` and `CambioGame.__init__` |
| `player_order()`, `setup_deck()`: `create_deck()`, `shuffle_deck()`, `deal_cards()` | `cambio_logic.py` |
| `initial_peak()` | `CambioApp.initial_peek()` |
| `play_game()` / `game_loop()` | `CambioApp.play_game()` |
| `take_turn()`, `draw_card()`, `replace_card()` | `CambioApp` methods, which call `CambioGame` |
| `check_action_card()`, `do_action()` | `check_action_card()` and `CambioApp.do_action()` |
| `peek_own_card()`, `peek_opp_card()`, `blind_swap()`, `look_swap()` | `CambioApp` methods |
| `check_stick()`, `stick_card()`, `check_match()`, `penalty()` | `CambioApp` + `CambioGame` |
| `check_cambio()` / `call_cambio()` | `CambioApp.call_cambio()`, `CambioGame.call_cambio()` / `end_turn()` |
| `end_game()`, `reveal_cards()`, `calculate_scores()`, `get_card_value()`, `determine_winner()` | `CambioApp.end_game()` + `cambio_logic.py` |
| `render_game()`, `create_table()`, `render_cards()`, `render_player_hands()`, `game_rules()`, `show_turn()`, `display_results()`, `show_player_score()`, `show_confetti()`, `show_kaboom()` | `CambioApp` drawing methods (`render_card()` draws a single card) |

New functions not in the chart: `give_card()` (after you stick someone else's card), `claim_stick()` (the first person to stick wins; anyone later gets a penalty), and refilling the deck from the discard pile.

## Rule decisions we made

These fill gaps the written rules didn't cover:

1. A drawn card you don't keep is discarded. Discarding a drawn action card lets you use its action (or skip it). You can also keep an action card in your hand instead, but then you don't get the action.
2. After every discard there is a stick window. It stays open until someone clicks **No more sticks – next**.
3. Only one stick per discard. Anyone who sticks after that gets a penalty card.
4. If you stick someone else's card, you give them one of your cards, face down, into the empty spot.
5. When a card leaves a hand, its spot stays empty, so the other cards don't move. Penalty cards go at the end.
6. The player who called Cambio is locked. Nobody can swap with their cards or stick them, and they can't stick either. Peeking at their cards is still allowed.
7. If the deck runs out, the discard pile (minus its top card) is shuffled into a new deck.
8. A tie for the lowest score means all tied players win.
9. A "Pass to Player X" screen between turns keeps peeks private.
