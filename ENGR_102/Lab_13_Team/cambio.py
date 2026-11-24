"""
cambio.py - Cambio card game in PyGame (hot-seat: everyone shares one screen)

Run:    python cambio.py
Needs:  pip install pygame
Rules:  press R at any time in the game.

The rules live in cambio_logic.py. This file draws everything and turns
clicks into game moves. Method names follow our hierarchy chart.
"""

import math
import random
import sys

import pygame

from cambio_logic import (
    ACTION_DESCRIPTIONS, MAX_PLAYERS, MIN_PLAYERS, CambioGame, Card,
    check_action_card, determine_winner, valid_player_count,
)

WIDTH, HEIGHT = 1400, 860
PLAY_W = 1100          # the table is on the left, the side panel on the right
PANEL_X = PLAY_W + 20
PANEL_W = WIDTH - PANEL_X - 20
FPS = 60

BG = (17, 21, 30)
FELT = (24, 112, 72)
FELT_LIGHT = (34, 130, 86)
TABLE_EDGE = (96, 58, 32)
PANEL = (30, 35, 48)
WHITE = (245, 245, 240)
CREAM = (252, 250, 242)
INK = (25, 25, 30)
RED = (200, 32, 44)
GOLD = (246, 198, 64)
GRAY = (140, 144, 156)
DIM = (90, 94, 108)
BLUE = (52, 96, 196)
BLUE_DARK = (30, 54, 128)
GREEN = (60, 170, 100)
ORANGE = (236, 120, 40)

# Where each player's hand sits on the table, for 2-6 players
SEATS = {
    2: [(550, 690), (550, 150)],
    3: [(550, 690), (230, 170), (870, 170)],
    4: [(550, 690), (170, 420), (550, 150), (930, 420)],
    5: [(550, 690), (170, 470), (310, 150), (790, 150), (930, 470)],
    6: [(360, 690), (150, 420), (360, 150), (740, 150), (950, 420), (740, 690)],
}
CENTER_CARD = (84, 120)
DECK_POS = (380, 360)
DISCARD_POS = (490, 360)
DRAWN_POS = (640, 360)
GAP = 8

# Secret ending: mash SPACE to flip the table (nobody wins)
FLIP_PRESSES = 10      # SPACE presses needed...
FLIP_WINDOW = 2.0      # ...within this many seconds
FLIP_ANIM = 3.2        # how long the flying-table animation plays (seconds)
GRAVITY = 1800.0       # pixels / second^2 for the flying table and cards
WOOD_DARK = (70, 42, 22)

RULES_TEXT = [
    ("GOAL", "Have the LOWEST total when the game ends."),
    ("VALUES", "Joker 0, Ace 1, 2-10 face value, Jack/Queen 10, black King 10, red King -1."),
    ("START", "Everyone gets 4 face-down cards and peeks at 2 of them. Remember them!"),
    ("YOUR TURN", "Draw a card. Swap it with one of your cards (no take-backs), or discard it."),
    ("ACTIONS", "Discarding a card you drew lets you use it: 7/8 peek at your card, 9/10 peek at "
                "someone else's, J/Q blind swap, black King look at 2 cards then swap if you want."),
    ("STICKING", "After any discard, anyone can stick: press your player number, then flip a card "
                 "with the same number/face. Wrong card, or too late (already stuck) = +1 card penalty. "
                 "Stick someone else's card and you give them one of yours."),
    ("CAMBIO", "Think you're lowest? Call Cambio instead of drawing. Everyone else gets one more turn "
               "and your cards are locked. Then all cards are revealed; lowest total wins."),
]


# ============================================================ drawing helpers

_font_cache = {}


def font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]


def blit_text(surf, text, size, color, pos, anchor="topleft"):
    img = font(size).render(text, True, color)
    rect = img.get_rect(**{anchor: pos})
    surf.blit(img, rect)
    return rect


def wrap_text(text, size, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = f"{line} {word}".strip()
        if font(size).size(test)[0] <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_suit(surf, suit, cx, cy, s, color):
    """Draw a suit symbol with shapes (fonts often lack the suit characters)."""
    r = s * 0.27
    
    if suit == "H":
        pygame.draw.circle(surf, color, (cx - r * 0.95, cy - r * 0.45), r)
        pygame.draw.circle(surf, color, (cx + r * 0.95, cy - r * 0.45), r)
        pygame.draw.polygon(surf, color, [(cx - r * 1.9, cy - r * 0.2),
                                          (cx + r * 1.9, cy - r * 0.2), (cx, cy + s * 0.5)])
    elif suit == "D":
        pygame.draw.polygon(surf, color, [(cx, cy - s * 0.5), (cx + s * 0.36, cy),
                                          (cx, cy + s * 0.5), (cx - s * 0.36, cy)])
    elif suit == "S":
        pygame.draw.circle(surf, color, (cx - r * 0.95, cy + r * 0.25), r)
        pygame.draw.circle(surf, color, (cx + r * 0.95, cy + r * 0.25), r)
        pygame.draw.polygon(surf, color, [(cx - r * 1.9, cy), (cx + r * 1.9, cy),
                                          (cx, cy - s * 0.5)])
        pygame.draw.polygon(surf, color, [(cx, cy + r * 0.2), (cx - r * 0.8, cy + s * 0.5),
                                          (cx + r * 0.8, cy + s * 0.5)])
    elif suit == "C":
        cr = r * 0.9
        pygame.draw.circle(surf, color, (cx, cy - r * 0.95), cr)
        pygame.draw.circle(surf, color, (cx - r * 1.0, cy + r * 0.3), cr)
        pygame.draw.circle(surf, color, (cx + r * 1.0, cy + r * 0.3), cr)
        pygame.draw.polygon(surf, color, [(cx, cy), (cx - r * 0.8, cy + s * 0.5),
                                          (cx + r * 0.8, cy + s * 0.5)])
    else:  # joker: a star
        pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5
            rad = s * 0.5 if k % 2 == 0 else s * 0.22
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        pygame.draw.polygon(surf, color, pts)


def render_card(surf, card, rect, face_up):
    """Draw one card, face up or face down."""
    rect = pygame.Rect(rect)
    radius = max(4, rect.w // 10)
    pygame.draw.rect(surf, (10, 40, 25), rect.move(3, 4), border_radius=radius)  # shadow
    if not face_up:
        pygame.draw.rect(surf, BLUE, rect, border_radius=radius)
        inner = rect.inflate(-rect.w * 0.22, -rect.w * 0.22)
        pygame.draw.rect(surf, BLUE_DARK, inner, border_radius=radius // 2)
        old_clip = surf.get_clip()
        surf.set_clip(inner)
        step = max(8, rect.w // 6)
        for k in range(-inner.h, inner.w + inner.h, step):
            pygame.draw.line(surf, BLUE, (inner.x + k, inner.y), (inner.x + k - inner.h, inner.bottom), 2)
            pygame.draw.line(surf, BLUE, (inner.x + k, inner.y), (inner.x + k + inner.h, inner.bottom), 2)
        surf.set_clip(old_clip)
        pygame.draw.rect(surf, WHITE, rect, 2, border_radius=radius)
        return
    pygame.draw.rect(surf, CREAM, rect, border_radius=radius)
    pygame.draw.rect(surf, (200, 196, 186), rect, 2, border_radius=radius)
    color = RED if card.is_red else INK
    label = "JK" if card.is_joker else card.rank
    size = int(rect.w * 0.42)
    blit_text(surf, label, size, color, (rect.x + rect.w * 0.09, rect.y + rect.h * 0.05))
    small = rect.w * 0.2
    if not card.is_joker:
        draw_suit(surf, card.suit, rect.x + rect.w * 0.2, rect.y + rect.h * 0.05 + size * 0.85, small, color)
    draw_suit(surf, "J" if card.is_joker else card.suit, rect.centerx, rect.centery + rect.h * 0.1,
              rect.w * 0.48, color)
    if card.is_joker:
        blit_text(surf, "JOKER", int(rect.w * 0.26), color, (rect.centerx, rect.bottom - rect.h * 0.06),
                  "midbottom")


class Button:
    def __init__(self, rect, text, on_click, enabled=True, color=BLUE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.enabled = enabled
        self.color = color

    def draw(self, surf, mouse):
        if not self.enabled:
            color = DIM
        elif self.rect.collidepoint(mouse):
            color = tuple(min(255, c + 35) for c in self.color)
        else:
            color = self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=9)
        size = 26 if font(26).size(self.text)[0] < self.rect.w - 12 else 21
        blit_text(surf, self.text, size, WHITE if self.enabled else GRAY, self.rect.center, "center")


# ============================================================ the game window

class CambioApp:
    def __init__(self, screen=None):
        pygame.init()
        pygame.display.set_caption("Cambio")
        self.screen = screen or pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.now = 0.0
        self.running = True
        self.reset()

    def reset(self):
        self.game = None
        self.state = "setup"
        self.input_text = ""
        self.error = ""
        self.show_rules = False
        self.revealed = set()   # (player, slot) cards shown face up to the current viewer
        self.flashes = {}       # (player, slot) -> time a wrongly stuck card stops showing
        self.drawn_card = None
        self.action = None
        self.selected = None    # first card picked for a swap
        self.selected2 = None   # second card picked for a look swap
        self.sticker = None
        self.give_target = None
        self.pass_player = None
        self.pass_message = ""
        self.after_pass = None
        self.peek_queue = []
        self.peeker = None
        self.final_scores = []
        self.winners = []
        self.confetti = []
        self.booms = []
        self.space_presses = []  # times of recent SPACE presses
        self.flipper = None
        self.flip_start = 0.0
        self.debris = []
        self.floor_cards = []

    # ------------------------------------------------------------ helpers
    @staticmethod
    def name(player):
        return f"Player {player + 1}"

    def say(self, message):
        self.game.log_event(message)

    @property
    def cur(self):
        return self.game.current_player

    def hand_rects(self, player):
        """Card slots in a grid of 4 columns, centered on the player's seat."""
        hand = self.game.hands[player]
        cw, ch = self.card_size
        rows = max(1, math.ceil(len(hand) / 4))
        width = 4 * cw + 3 * GAP
        height = rows * ch + (rows - 1) * GAP
        cx, cy = self.seats[player]
        x0, y0 = cx - width // 2, cy - height // 2
        return [pygame.Rect(x0 + (i % 4) * (cw + GAP), y0 + (i // 4) * (ch + GAP), cw, ch)
                for i in range(len(hand))]

    def card_at(self, pos):
        for p in range(self.game.num_players):
            for i, rect in enumerate(self.hand_rects(p)):
                if rect.collidepoint(pos) and self.game.hands[p][i] is not None:
                    return p, i
        return None

    def active_player(self):
        """Whose seat is highlighted right now (None = nobody / everybody)."""
        if self.state == "initial_peek":
            return self.peeker
        if self.state in ("stick_pick", "stick_give"):
            return self.sticker
        if self.state in ("setup", "pass", "stick", "results", "flipped", "flip_results"):
            return None
        return self.cur

    def action_possible(self, action):
        g, cur = self.game, self.cur
        own = g.hand_size(cur) > 0
        opponents = [p for p in g.opponents(cur) if g.hand_size(p) > 0]
        if action == "peek_own":
            return own
        if action == "peek_opp":
            return bool(opponents)
        return own and any(not g.is_locked(p) for p in opponents)

    def card_target_ok(self, p, i):
        """Can this card be clicked right now?"""
        g, st = self.game, self.state
        if g is None or i >= len(g.hands[p]) or g.hands[p][i] is None:
            return False
        if st == "initial_peek":
            return p == self.peeker and (p, i) not in self.revealed and len(self.revealed) < 2
        if st in ("drawn", "pick_own"):
            return p == self.cur
        if st == "pick_opp":
            if p == self.cur:
                return False
            return not (self.action in ("blind_swap", "look_swap") and g.is_locked(p))
        if st == "stick_pick":
            return not g.is_locked(p)
        if st == "stick_give":
            return p == self.sticker
        return False

    # ------------------------------------------------------------ setup
    def player_count(self):
        """Read the typed number of players (must be 2-6)."""
        n = valid_player_count(self.input_text)
        if n is None:
            self.error = f"Please type a whole number from {MIN_PLAYERS} to {MAX_PLAYERS}."
            self.input_text = ""
            return
        self.initialize_game(n)

    def initialize_game(self, num_players):
        self.game = CambioGame(num_players)   # creates, shuffles and deals the deck
        self.seats = SEATS[num_players]
        cw = 64 if num_players <= 4 else 56
        self.card_size = (cw, int(cw * 1.43))
        order = " -> ".join(str(p + 1) for p in self.game.order)
        self.say(f"New game with {num_players} players. Turn order: {order}.")
        self.peek_queue = list(self.game.order)
        self.next_initial_peek()

    def pass_to(self, player, message, then):
        """Cover the screen so the next player can take the seat privately."""
        self.revealed.clear()
        self.selected = self.selected2 = None
        self.state = "pass"
        self.pass_player = player
        self.pass_message = message
        self.after_pass = then

    def continue_pass(self):
        then, self.after_pass = self.after_pass, None
        if then:
            then()

    def next_initial_peek(self):
        if not self.peek_queue:
            self.start_turn()
            return
        p = self.peek_queue.pop(0)
        self.pass_to(p, "Time to peek at 2 of your cards.", lambda: self.initial_peek(p))

    def initial_peek(self, player):
        self.state = "initial_peek"
        self.peeker = player
        self.revealed.clear()

    def finish_initial_peek(self):
        self.revealed.clear()
        self.next_initial_peek()

    # ------------------------------------------------------------ a turn
    def start_turn(self):
        msg = "It's your turn."
        if self.game.cambio_caller is not None:
            msg = f"LAST TURN! {self.name(self.game.cambio_caller)} called Cambio."
        self.pass_to(self.cur, msg, self.take_turn)

    def take_turn(self):
        self.state = "turn"
        self.drawn_card = None
        self.action = None

    def draw_card(self):
        card = self.game.draw_card()
        if card is None:
            self.say("There are no cards left to draw, so the game ends now.")
            self.end_game()
            return
        self.drawn_card = card
        self.state = "drawn"

    def replace_card(self, index):
        old = self.game.replace_card(self.cur, index, self.drawn_card)
        self.say(f"{self.name(self.cur)} kept the drawn card and discarded a {old}.")
        self.drawn_card = None
        self.open_stick_window()

    def discard_drawn(self):
        card, self.drawn_card = self.drawn_card, None
        self.game.discard(card)
        self.say(f"{self.name(self.cur)} discarded a {card}.")
        self.action = check_action_card(card)
        if self.action:
            self.state = "action_offer"
        else:
            self.open_stick_window()

    def do_action(self):
        self.state = "pick_opp" if self.action == "peek_opp" else "pick_own"

    def skip_action(self):
        self.say(f"{self.name(self.cur)} didn't use the action.")
        self.open_stick_window()

    def peek_own_card(self, i):
        self.revealed = {(self.cur, i)}
        self.state = "reveal"
        self.say(f"{self.name(self.cur)} peeked at one of their own cards.")

    def peek_opp_card(self, p, i):
        self.revealed = {(p, i)}
        self.state = "reveal"
        self.say(f"{self.name(self.cur)} peeked at one of {self.name(p)}'s cards.")

    def blind_swap(self, p, i):
        own = self.selected[1]
        self.game.blind_swap(self.cur, own, p, i)
        self.say(f"{self.name(self.cur)} blind swapped a card with {self.name(p)}.")
        self.open_stick_window()

    def look_swap(self, do_swap):
        (me, mine), (p, i) = self.selected, self.selected2
        if do_swap:
            self.game.look_swap(me, mine, p, i)
            self.say(f"{self.name(me)} looked, then swapped a card with {self.name(p)}.")
        else:
            self.say(f"{self.name(me)} looked at a card of {self.name(p)}'s but didn't swap.")
        self.open_stick_window()

    def click_card(self, p, i):
        st = self.state
        if st == "initial_peek":
            self.revealed.add((p, i))
        elif st == "drawn":
            self.replace_card(i)
        elif st == "pick_own":
            if self.action == "peek_own":
                self.peek_own_card(i)
            else:
                self.selected = (p, i)
                self.state = "pick_opp"
        elif st == "pick_opp":
            if self.action == "peek_opp":
                self.peek_opp_card(p, i)
            elif self.action == "blind_swap":
                self.blind_swap(p, i)
            else:
                self.selected2 = (p, i)
                self.revealed = {self.selected, (p, i)}
                self.state = "look_decide"
        elif st == "stick_pick":
            self.stick_card(p, i)
        elif st == "stick_give":
            owner, slot = self.give_target
            self.game.give_card(self.sticker, i, owner, slot)
            self.say(f"{self.name(self.sticker)} gave {self.name(owner)} one of their cards.")
            self.state = "stick"

    # ------------------------------------------------------------ sticking
    def open_stick_window(self):
        self.revealed.clear()
        self.selected = self.selected2 = None
        self.action = None
        self.state = "stick"

    def check_stick(self, player):
        """A player presses their Stick button / number key."""
        if self.state != "stick" or player >= self.game.num_players:
            return
        top = self.game.top_discard()
        result = self.game.claim_stick(player)
        if result == "late":
            self.say(f"{self.name(player)} was too late - that {top.rank} was already stuck. Penalty: +1 card!")
        elif result == "ok":
            self.sticker = player
            self.state = "stick_pick"

    def stick_card(self, owner, i):
        g, s = self.game, self.sticker
        card = g.hands[owner][i]
        result = g.stick_card(s, owner, i)
        self.state = "stick"
        if result == "match":
            self.say(f"{self.name(s)} stuck their {card}! One card fewer.")
        elif result == "match_opponent":
            self.say(f"{self.name(s)} stuck {self.name(owner)}'s {card}!")
            if g.hand_size(s) > 0:
                self.give_target = (owner, i)
                self.state = "stick_give"
        elif result == "miss":
            self.flashes[(owner, i)] = self.now + 2.5
            self.say(f"{self.name(s)} flipped a {card} - no match! Penalty: +1 card.")

    def give_up_stick(self):
        self.game.penalty(self.sticker)
        self.say(f"{self.name(self.sticker)} couldn't find a match. Penalty: +1 card.")
        self.state = "stick"

    def finish_turn(self):
        self.revealed.clear()
        self.sticker = None
        if self.game.end_turn():
            self.end_game()
        else:
            self.start_turn()

    # ------------------------------------------------------------ cambio / end
    def call_cambio(self):
        p = self.cur
        self.game.call_cambio(p)
        self.say(f"{self.name(p)} called CAMBIO! Everyone else gets one last turn. "
                 f"{self.name(p)}'s cards are locked.")
        self.finish_turn()

    def reveal_cards(self):
        self.revealed = {(p, i) for p in range(self.game.num_players)
                         for i in range(len(self.game.hands[p]))}

    def end_game(self):
        self.game.over = True
        self.state = "results"
        self.reveal_cards()
        self.final_scores = self.game.scores()       # calculate_scores()
        self.winners = determine_winner(self.final_scores)
        names = " & ".join(self.name(p) for p in self.winners)
        self.say(f"{names} {'win' if len(self.winners) > 1 else 'wins'} with "
                 f"{self.final_scores[self.winners[0]]} points!")
        with open("winners.txt", "a") as file:
            file.write(f"{names} {'win' if len(self.winners) > 1 else 'wins'} with" + f"{self.final_scores[self.winners[0]]} points!")
        
        self.results_start = self.now
        self.confetti = []
        losers = [p for p in range(self.game.num_players) if p not in self.winners]
        self.booms = [{"player": p, "next": self.now + 0.4 + k * 0.5, "start": None, "debris": []}
                      for k, p in enumerate(losers)]
        for p in self.winners:
            self.spawn_confetti(self.seats[p], 120)

    # ------------------------------------------------------------ buttons
    def make_buttons(self):
        st = self.state
        if st in ("pass", "flipped"):
            return []
        bx, bw, y = PANEL_X, PANEL_W, 230
        buttons = []

        def add(text, fn, enabled=True, color=BLUE):
            nonlocal y
            buttons.append(Button((bx, y, bw, 46), text, fn, enabled, color))
            y += 56

        if st == "setup":
            return [Button((WIDTH // 2 - 110, 520, 220, 54), "Start game", self.player_count, color=GREEN),
                    Button((WIDTH // 2 - 110, 586, 220, 44), "Rules (R)", self.toggle_rules, color=DIM)]
        buttons.append(Button((PANEL_X + PANEL_W - 110, 22, 110, 36), "Rules (R)", self.toggle_rules, color=DIM))
        g = self.game
        if st == "initial_peek":
            need = min(2, g.hand_size(self.peeker))
            add("Done - hide them", self.finish_initial_peek, len(self.revealed) >= need, GREEN)
        elif st == "turn":
            add("Draw a card", self.draw_card, color=GREEN)
            add("Call CAMBIO!", self.call_cambio, g.can_call_cambio(), ORANGE)
        elif st == "drawn":
            action = check_action_card(self.drawn_card)
            add("Discard + use action" if action else "Discard it", self.discard_drawn)
        elif st == "action_offer":
            ok = self.action_possible(self.action)
            add(ACTION_DESCRIPTIONS[self.action] if ok else "No one to target", self.do_action, ok, GREEN)
            add("Skip action", self.skip_action, color=DIM)
        elif st in ("pick_own", "pick_opp"):
            add("Skip action", self.skip_action, color=DIM)
        elif st == "reveal":
            add("Done looking", self.open_stick_window, color=GREEN)
        elif st == "look_decide":
            add("Swap them", lambda: self.look_swap(True), color=GREEN)
            add("Don't swap", lambda: self.look_swap(False), color=DIM)
        elif st == "stick":
            half = (bw - 10) // 2
            for p in range(g.num_players):
                col, row = p % 2, p // 2
                rect = (bx + col * (half + 10), y + row * 54, half, 46)
                buttons.append(Button(rect, f"[{p + 1}] P{p + 1} stick", lambda p=p: self.check_stick(p),
                                      not g.is_locked(p), ORANGE))
            y += math.ceil(g.num_players / 2) * 54 + 10
            add("No more sticks - next", self.finish_turn, color=GREEN)
        elif st == "stick_pick":
            add("Give up (+1 penalty)", self.give_up_stick, color=DIM)
        elif st in ("results", "flip_results"):
            add("Play again", self.reset, color=GREEN)
            add("Quit", self.quit, color=DIM)
        return buttons

    def toggle_rules(self):
        self.show_rules = not self.show_rules

    def quit(self):
        self.running = False

    # ------------------------------------------------------------ input
    def handle_click(self, pos):
        if self.show_rules:
            self.show_rules = False
            return
        for b in self.make_buttons():
            if b.enabled and b.rect.collidepoint(pos):
                b.on_click()
                return
        if self.state == "pass":
            self.continue_pass()
            return
        if self.game and self.state not in ("setup", "results", "flipped", "flip_results"):
            hit = self.card_at(pos)
            if hit and self.card_target_ok(*hit):
                self.click_card(*hit)

    def handle_key(self, event):
        if event.key == pygame.K_SPACE and self.register_space():
            return  # the table just got flipped
        if event.key == pygame.K_r:
            self.toggle_rules()
            return
        if self.show_rules:
            if event.key == pygame.K_ESCAPE:
                self.show_rules = False
            return
        if self.state == "setup":
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.player_count()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.input_text) < 3:
                self.input_text += event.unicode
                self.error = ""
        elif self.state == "pass" and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.continue_pass()
        elif self.state == "stick" and event.unicode in "123456" and event.unicode:
            self.check_stick(int(event.unicode) - 1)

    # ------------------------------------------------------------ rendering
    def render_game(self):
        surf = self.screen
        surf.fill(BG)
        if self.state == "setup":
            self.draw_setup()
        elif self.state == "flipped":
            self.draw_flip()
            self.draw_panel()
        elif self.state == "flip_results":
            self.draw_flip_results()
            self.draw_panel()
        else:
            self.create_table()
            self.render_piles()
            self.render_player_hands()
            self.draw_panel()
            if self.state == "results":
                self.display_results()
            if self.state == "pass":
                self.draw_pass_screen()
        if self.show_rules:
            self.game_rules()

    def draw_setup(self):
        s = self.screen
        for k in range(5):  # a fan of cards for decoration
            ang = -24 + k * 12
            card_surf = pygame.Surface((90, 128), pygame.SRCALPHA)
            render_card(card_surf, Card(["K", "7", "JOKER", "A", "K"][k], ["H", "S", "R", "D", "C"][k]),
                        (0, 0, 86, 123), True)
            rot = pygame.transform.rotozoom(card_surf, -ang, 1)
            s.blit(rot, rot.get_rect(center=(WIDTH // 2 + (k - 2) * 52, 200 + abs(k - 2) * 10)))
        blit_text(s, "CAMBIO", 110, GOLD, (WIDTH // 2, 300), "midtop")
        blit_text(s, "Lowest hand wins. Remember your cards!", 32, GRAY, (WIDTH // 2, 385), "midtop")
        blit_text(s, f"How many players? ({MIN_PLAYERS}-{MAX_PLAYERS})", 36, WHITE, (WIDTH // 2, 430), "midtop")
        box = pygame.Rect(WIDTH // 2 - 60, 466, 120, 44)
        pygame.draw.rect(s, PANEL, box, border_radius=8)
        pygame.draw.rect(s, GOLD, box, 2, border_radius=8)
        cursor = "|" if int(self.now * 2) % 2 == 0 else ""
        blit_text(s, self.input_text + cursor, 40, WHITE, box.center, "center")
        if self.error:
            blit_text(s, self.error, 28, (255, 120, 120), (WIDTH // 2, 642), "midtop")
        blit_text(s, "Type a number and press Enter", 24, GRAY, (WIDTH // 2, 680), "midtop")
        mouse = pygame.mouse.get_pos()
        for b in self.make_buttons():
            b.draw(s, mouse)

    def create_table(self, surf=None, table=None):
        s = surf or self.screen
        table = table or pygame.Rect(20, 20, PLAY_W - 40, HEIGHT - 40)
        pygame.draw.rect(s, TABLE_EDGE, table, border_radius=120)
        felt = table.inflate(-28, -28)
        pygame.draw.rect(s, FELT, felt, border_radius=105)
        pygame.draw.ellipse(s, FELT_LIGHT, felt.inflate(-300, -320), 3)

    def render_piles(self):
        s, g = self.screen, self.game
        w, h = CENTER_CARD
        deck_rect = pygame.Rect(*DECK_POS, w, h)
        if g.deck:
            for k in range(min(3, len(g.deck)) - 1, -1, -1):
                render_card(s, None, deck_rect.move(-k * 2, -k * 2), False)
        else:
            pygame.draw.rect(s, FELT_LIGHT, deck_rect, 2, border_radius=8)
        blit_text(s, f"Deck ({len(g.deck)})", 22, WHITE, (deck_rect.centerx, deck_rect.bottom + 8), "midtop")

        disc_rect = pygame.Rect(*DISCARD_POS, w, h)
        top = g.top_discard()
        if self.state in ("stick", "stick_pick", "stick_give") and top:
            pulse = 4 + 3 * math.sin(self.now * 6)
            pygame.draw.rect(s, GOLD, disc_rect.inflate(pulse * 2 + 6, pulse * 2 + 6), border_radius=12)
        if top:
            render_card(s, top, disc_rect, True)
        else:
            pygame.draw.rect(s, FELT_LIGHT, disc_rect, 2, border_radius=8)
        blit_text(s, "Discard", 22, WHITE, (disc_rect.centerx, disc_rect.bottom + 8), "midtop")

        if self.drawn_card is not None:
            drawn = pygame.Rect(*DRAWN_POS, w, h).move(0, -6 + 3 * math.sin(self.now * 3))
            pygame.draw.rect(s, GOLD, drawn.inflate(10, 10), border_radius=12)
            render_card(s, self.drawn_card, drawn, True)
            blit_text(s, "You drew", 22, GOLD, (drawn.centerx, DRAWN_POS[1] + h + 8), "midtop")

        prompt = self.state_prompt()
        if prompt:
            for k, line in enumerate(wrap_text(prompt, 26, 440)[:3]):
                blit_text(s, line, 26, WHITE, (DISCARD_POS[0] + w // 2 + 30, 515 + k * 24), "midtop")

    def render_player_hands(self):
        s, g = self.screen, self.game
        mouse = pygame.mouse.get_pos()
        active = self.active_player()
        for p in range(g.num_players):
            rects = self.hand_rects(p)
            cx = self.seats[p][0]
            top = rects[0].top if rects else self.seats[p][1]
            is_turn = p == active
            if is_turn and rects:
                area = rects[0].unionall(rects).inflate(22, 22)
                pygame.draw.rect(s, GOLD, area, 3, border_radius=12)
            label = self.name(p)
            color = GOLD if is_turn else WHITE
            if g.is_locked(p) and self.state != "results":
                label += "  - LOCKED"
                color = (255, 150, 90)
            if self.state == "results":
                label += f"   Score: {self.final_scores[p]}"
                color = GOLD if p in self.winners else WHITE
            blit_text(s, label, 26, color, (cx, top - 16), "midbottom")
            shake = self.kaboom_shake(p)
            for i, rect in enumerate(rects):
                card = g.hands[p][i]
                if card is None:
                    pygame.draw.rect(s, FELT_LIGHT, rect, 2, border_radius=6)
                    continue
                face_up = (p, i) in self.revealed or self.flashes.get((p, i), 0) > self.now
                clickable = self.card_target_ok(p, i)
                r = rect.move(*shake)
                if clickable and rect.collidepoint(mouse):
                    r = r.move(0, -8)
                if (p, i) in (self.selected, self.selected2):
                    pygame.draw.rect(s, GOLD, r.inflate(10, 10), border_radius=9)
                elif clickable:
                    pygame.draw.rect(s, (255, 255, 200), r.inflate(6, 6), 2, border_radius=8)
                render_card(s, card, r, face_up)
                if self.flashes.get((p, i), 0) > self.now:
                    pygame.draw.rect(s, RED, r.inflate(6, 6), 3, border_radius=8)
                if g.is_locked(p) and self.state != "results":
                    veil = pygame.Surface(r.size, pygame.SRCALPHA)
                    veil.fill((0, 0, 0, 90))
                    s.blit(veil, r)

    def state_prompt(self):
        st, g = self.state, self.game
        top = g.top_discard()
        if st == "initial_peek":
            return f"{self.name(self.peeker)}: click 2 of your cards to memorize them."
        if st == "turn":
            return f"{self.name(self.cur)}: draw a card, or call Cambio if you think you have the lowest total."
        if st == "drawn":
            text = "Click one of your cards to swap the drawn card in, or discard it."
            action = check_action_card(self.drawn_card)
            if action:
                text += f" Discarding lets you: {ACTION_DESCRIPTIONS[action].lower()}."
            return text
        if st == "action_offer":
            return f"You discarded a {top.rank}: {ACTION_DESCRIPTIONS[self.action].lower()}?"
        if st == "pick_own":
            return "Click one of YOUR cards to " + ("peek at." if self.action == "peek_own" else "swap away.")
        if st == "pick_opp":
            return "Click another player's card to " + ("peek at." if self.action == "peek_opp" else "swap with.")
        if st == "reveal":
            return "Memorize it, then press Done."
        if st == "look_decide":
            return "Both cards are shown. Swap them?"
        if st == "stick" and top:
            return f"STICK? Anyone with a {top.rank}: press your number (1-{g.num_players}), then click the card."
        if st == "stick_pick":
            return f"{self.name(self.sticker)}: click the card that matches the {top.rank} - yours or anyone's."
        if st == "stick_give":
            return (f"{self.name(self.sticker)}: click one of your cards to give to "
                    f"{self.name(self.give_target[0])}.")
        return ""

    def show_turn(self, y):
        s, g = self.screen, self.game
        if self.state in ("results", "flipped", "flip_results"):
            blit_text(s, "Game over", 34, GOLD, (PANEL_X, y))
            return
        if self.state == "initial_peek":
            blit_text(s, f"{self.name(self.peeker)} peeking", 34, GOLD, (PANEL_X, y))
            blit_text(s, "Everyone peeks before play", 24, GRAY, (PANEL_X, y + 38))
            return
        blit_text(s, f"{self.name(self.cur)}'s turn", 34, GOLD, (PANEL_X, y))
        if g.cambio_caller is not None:
            left = g.final_turns_left
            blit_text(s, f"CAMBIO called by {self.name(g.cambio_caller)}", 24, ORANGE, (PANEL_X, y + 38))
            blit_text(s, f"{left} last turn{'s' if left != 1 else ''} left", 24, ORANGE, (PANEL_X, y + 62))
        else:
            blit_text(s, "Lowest total wins", 24, GRAY, (PANEL_X, y + 38))

    def show_player_score(self, y):
        s = self.screen
        blit_text(s, "Final scores", 28, WHITE, (PANEL_X, y))
        ranked = sorted(range(self.game.num_players), key=lambda p: self.final_scores[p])
        for k, p in enumerate(ranked):
            color = GOLD if p in self.winners else WHITE
            blit_text(s, f"{self.name(p)}", 26, color, (PANEL_X, y + 32 + k * 26))
            blit_text(s, str(self.final_scores[p]), 26, color, (PANEL_X + PANEL_W, y + 32 + k * 26), "topright")

    def draw_panel(self):
        s = self.screen
        pygame.draw.rect(s, PANEL, (PLAY_W, 0, WIDTH - PLAY_W, HEIGHT))
        blit_text(s, "CAMBIO", 46, GOLD, (PANEL_X, 24))
        self.show_turn(100)
        mouse = pygame.mouse.get_pos()
        buttons = self.make_buttons()
        for b in buttons:
            b.draw(s, mouse)
        log_top = max([b.rect.bottom for b in buttons] + [420]) + 20
        if self.state == "results":
            self.show_player_score(log_top)
            log_top += 50 + 26 * self.game.num_players
        blit_text(s, "What happened", 24, GRAY, (PANEL_X, log_top))
        lines = []
        for msg in self.game.log[-8:]:
            lines += [(line, msg is self.game.log[-1]) for line in wrap_text(msg, 21, PANEL_W)]
        max_lines = max(0, (HEIGHT - 20 - (log_top + 26)) // 19)
        for k, (line, newest) in enumerate(lines[-max_lines:] if max_lines else []):
            blit_text(s, line, 21, WHITE if newest else GRAY, (PANEL_X, log_top + 26 + k * 19))

    def draw_pass_screen(self):
        s = self.screen
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((8, 10, 16, 235))
        s.blit(veil, (0, 0))
        blit_text(s, f"Pass to {self.name(self.pass_player)}", 80, GOLD, (WIDTH // 2, HEIGHT // 2 - 80), "center")
        blit_text(s, self.pass_message, 36, WHITE, (WIDTH // 2, HEIGHT // 2), "center")
        blit_text(s, "Everyone else, look away!", 28, GRAY, (WIDTH // 2, HEIGHT // 2 + 50), "center")
        blit_text(s, f"Click or press SPACE when {self.name(self.pass_player)} is ready",
                  26, GRAY, (WIDTH // 2, HEIGHT // 2 + 110), "center")

    def game_rules(self):
        s = self.screen
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 200))
        s.blit(veil, (0, 0))
        box = pygame.Rect(170, 120, WIDTH - 340, 610)
        pygame.draw.rect(s, PANEL, box, border_radius=16)
        pygame.draw.rect(s, GOLD, box, 2, border_radius=16)
        blit_text(s, "How to play Cambio", 54, GOLD, (box.centerx, box.y + 24), "midtop")
        y = box.y + 90
        for head, text in RULES_TEXT:
            blit_text(s, head, 26, GOLD, (box.x + 40, y))
            for line in wrap_text(text, 26, box.w - 220):
                blit_text(s, line, 26, WHITE, (box.x + 180, y))
                y += 26
            y += 12
        blit_text(s, "Click anywhere or press R to close", 24, GRAY, (box.centerx, box.bottom - 20), "midbottom")

    # ------------------------------------------------------------ results animations
    def display_results(self):
        s = self.screen
        names = " & ".join(self.name(p) for p in self.winners)
        verb = "WIN!" if len(self.winners) > 1 else "WINS!"
        banner = pygame.Rect(0, 0, 560, 84)
        banner.center = (PLAY_W // 2, 530)
        pygame.draw.rect(s, (20, 24, 34), banner, border_radius=16)
        pygame.draw.rect(s, GOLD, banner, 3, border_radius=16)
        blit_text(s, f"{names} {verb}", 44 if len(self.winners) < 3 else 32, GOLD,
                  (banner.centerx, banner.centery - 12), "center")
        blit_text(s, f"with {self.final_scores[self.winners[0]]} points", 26, WHITE,
                  (banner.centerx, banner.centery + 22), "center")
        self.show_kaboom()
        self.show_confetti()

    def spawn_confetti(self, origin, count):
        colors = [GOLD, RED, (80, 200, 255), (120, 230, 120), (240, 120, 220), WHITE]
        for _ in range(count):
            ang = random.uniform(-math.pi, 0)
            speed = random.uniform(150, 520)
            self.confetti.append({
                "x": origin[0], "y": origin[1], "vx": math.cos(ang) * speed, "vy": math.sin(ang) * speed,
                "color": random.choice(colors), "w": random.randint(5, 10), "h": random.randint(8, 14),
                "angle": random.uniform(0, 360), "spin": random.uniform(-400, 400),
            })

    def update_effects(self, dt):
        if self.state == "flipped" and self.now - self.flip_start >= FLIP_ANIM:
            self.state = "flip_results"
        if self.state != "results":
            return
        for _ in range(3):  # gentle rain from the top
            self.spawn_confetti((random.uniform(30, PLAY_W - 30), -10), 1)
            self.confetti[-1]["vy"] = random.uniform(40, 120)
            self.confetti[-1]["vx"] = random.uniform(-40, 40)
        for c in self.confetti:
            c["vy"] += 300 * dt
            c["vx"] *= 0.99
            c["x"] += c["vx"] * dt + math.sin(self.now * 3 + c["angle"]) * 0.6
            c["y"] += min(c["vy"], 260) * dt if c["vy"] > 0 else c["vy"] * dt
            c["angle"] += c["spin"] * dt
        self.confetti = [c for c in self.confetti if c["y"] < HEIGHT + 20][-900:]
        for boom in self.booms:
            if self.now >= boom["next"]:
                boom["start"] = self.now
                boom["next"] = self.now + 3.0
                cx, cy = self.seats[boom["player"]]
                boom["debris"] = [{"x": cx, "y": cy, "vx": math.cos(a) * v, "vy": math.sin(a) * v}
                                  for a, v in ((random.uniform(0, 2 * math.pi), random.uniform(120, 420))
                                               for _ in range(40))]
            for d in boom["debris"]:
                d["vy"] += 400 * dt
                d["x"] += d["vx"] * dt
                d["y"] += d["vy"] * dt

    def show_confetti(self):
        for c in self.confetti:
            piece = pygame.Surface((c["w"], c["h"]), pygame.SRCALPHA)
            piece.fill(c["color"])
            rot = pygame.transform.rotate(piece, c["angle"])
            self.screen.blit(rot, rot.get_rect(center=(c["x"], c["y"])))

    def kaboom_shake(self, player):
        for boom in self.booms:
            if boom["player"] == player and boom["start"] is not None and self.now - boom["start"] < 0.5:
                return random.randint(-6, 6), random.randint(-6, 6)
        return 0, 0

    def show_kaboom(self):
        s = self.screen
        fx = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for boom in self.booms:
            if boom["start"] is None:
                continue
            t = self.now - boom["start"]
            if t > 1.6:
                continue
            cx, cy = self.seats[boom["player"]]
            fade = max(0.0, 1 - t / 1.2)
            if t < 1.2:
                pygame.draw.circle(fx, (255, 240, 120, int(220 * fade)), (cx, cy), int(30 + 140 * t))
                pygame.draw.circle(fx, (255, 140, 30, int(200 * fade)), (cx, cy), int(20 + 100 * t))
                pygame.draw.circle(fx, (200, 40, 20, int(180 * fade)), (cx, cy), int(10 + 60 * t))
                pygame.draw.circle(fx, (255, 255, 255, int(160 * fade)), (cx, cy), int(40 + 260 * t), 4)
            for d in boom["debris"]:
                pygame.draw.circle(fx, (90, 70, 60, int(255 * max(0, 1 - t / 1.6))), (d["x"], d["y"]), 4)
        s.blit(fx, (0, 0))
        for boom in self.booms:
            if boom["start"] is not None and self.now - boom["start"] < 1.0:
                t = self.now - boom["start"]
                cx, cy = self.seats[boom["player"]]
                cx = min(max(cx, 170), PLAY_W - 170)  # keep the text on screen
                size = int(40 + 50 * min(1, t * 4))
                jitter = random.randint(-3, 3)
                blit_text(s, "KABOOM!", size, (40, 10, 0), (cx + 3 + jitter, cy - 40 + 3), "center")
                blit_text(s, "KABOOM!", size, ORANGE, (cx + jitter, cy - 40), "center")

    # ------------------------------------------------------------ secret ending: flip the table
    def register_space(self):
        """Count SPACE presses. FLIP_PRESSES of them within FLIP_WINDOW seconds flips
        the table. Returns True if this press flipped it."""
        if self.game is None or self.state in ("setup", "results", "flipped", "flip_results"):
            return False
        self.space_presses = [t for t in self.space_presses if self.now - t <= FLIP_WINDOW]
        self.space_presses.append(self.now)
        if len(self.space_presses) >= FLIP_PRESSES:
            self.flip_table()
            return True
        return False

    def flip_table(self):
        """Whoever is playing right now rage-quits: everything flies and nobody wins."""
        flipper = self.active_player()
        if flipper is None:
            flipper = self.pass_player if self.state == "pass" else self.cur
        self.flipper = flipper
        self.space_presses = []
        self.show_rules = False
        self.say(f"{self.name(flipper)} flipped the table! Nobody wins.")

        # Each piece of debris: a picture, where it starts, its speed and its spin.
        # The table goes first so the cards fly in front of it.
        table_rect = pygame.Rect(20, 20, PLAY_W - 40, HEIGHT - 40)
        top = pygame.Surface(table_rect.size, pygame.SRCALPHA)
        self.create_table(top, top.get_rect())
        self.debris = [{"surf": top, "under": self.table_underside(table_rect.size),
                        "x": table_rect.centerx, "y": table_rect.centery,
                        "vx": 0.0, "vy": -1000.0, "spin": 35.0, "table": True}]

        def throw(card, rect, face_up):
            surf = pygame.Surface((rect.w + 4, rect.h + 5), pygame.SRCALPHA)
            render_card(surf, card, (0, 0, rect.w, rect.h), face_up)
            self.debris.append({"surf": surf, "x": rect.centerx, "y": rect.centery,
                                "vx": random.uniform(-500, 500), "vy": random.uniform(-1400, -650),
                                "spin": random.uniform(-600, 600)})

        g = self.game
        for p in range(g.num_players):
            for i, rect in enumerate(self.hand_rects(p)):
                if g.hands[p][i] is not None:
                    throw(g.hands[p][i], rect, (p, i) in self.revealed)
        w, h = CENTER_CARD
        for k in range(min(6, len(g.deck))):
            throw(None, pygame.Rect(*DECK_POS, w, h), False)
        if g.top_discard():
            throw(g.top_discard(), pygame.Rect(*DISCARD_POS, w, h), True)
        if self.drawn_card is not None:
            throw(self.drawn_card, pygame.Rect(*DRAWN_POS, w, h), True)

        # Where the cards end up on the floor for the game-over screen
        self.floor_cards = [(random.uniform(70, PLAY_W - 70), random.uniform(430, 800),
                             random.uniform(0, 360)) for _ in range(len(self.debris) - 1)]
        self.drawn_card = None
        self.revealed.clear()
        self.selected = self.selected2 = None
        self.flip_start = self.now
        self.state = "flipped"

    @staticmethod
    def table_underside(size):
        """The bottom of the table: bare wood, braces and four legs."""
        w, h = size
        under = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(under, WOOD_DARK, (0, 0, w, h), border_radius=120)
        for k in range(1, 8):  # planks
            y = h * k // 8
            pygame.draw.line(under, (56, 33, 17), (40, y), (w - 40, y), 3)
        pygame.draw.line(under, TABLE_EDGE, (140, 140), (w - 140, h - 140), 18)
        pygame.draw.line(under, TABLE_EDGE, (w - 140, 140), (140, h - 140), 18)
        for x, y in ((140, 140), (w - 140, 140), (140, h - 140), (w - 140, h - 140)):
            pygame.draw.circle(under, (40, 24, 12), (x, y), 46)
            pygame.draw.circle(under, TABLE_EDGE, (x, y), 34)
        return under

    def draw_flip(self):
        s = self.screen
        t = self.now - self.flip_start
        s.fill(BG)
        sx, sy = (random.randint(-12, 12), random.randint(-12, 12)) if t < 0.35 else (0, 0)
        for d in self.debris:
            x = d["x"] + d["vx"] * t + sx
            y = d["y"] + d["vy"] * t + 0.5 * GRAVITY * t * t + sy
            if y > HEIGHT + 900:
                continue
            if d.get("table"):
                # flip end over end: squash it, and show the underside once it turns over
                tilt = math.cos(2.6 * t)
                img = d["surf"] if tilt >= 0 else d["under"]
                w, h = img.get_size()
                img = pygame.transform.scale(img, (w, max(2, int(h * abs(tilt)))))
                img = pygame.transform.rotate(img, d["spin"] * t)
            else:
                img = pygame.transform.rotate(d["surf"], d["spin"] * t)
            s.blit(img, img.get_rect(center=(int(x), int(y))))
        if t > 0.35:
            pop = min(1.0, (t - 0.35) * 5)
            blit_text(s, "TABLE FLIPPED!", int(60 + 50 * pop), (40, 10, 0), (PLAY_W // 2 + 4, 334), "center")
            blit_text(s, "TABLE FLIPPED!", int(60 + 50 * pop), GOLD, (PLAY_W // 2, 330), "center")
            blit_text(s, f"{self.name(self.flipper)} has had enough.", 36, WHITE, (PLAY_W // 2, 400), "center")

    def draw_flip_results(self):
        s = self.screen
        floor = pygame.Rect(20, 20, PLAY_W - 40, HEIGHT - 40)
        pygame.draw.rect(s, (46, 36, 30), floor, border_radius=24)
        for k in range(1, 12):  # floorboards
            x = floor.x + floor.w * k // 12
            pygame.draw.line(s, (38, 29, 24), (x, floor.y + 10), (x, floor.bottom - 10), 3)
        # the upside-down table, legs in the air
        slab = pygame.Rect(0, 0, 640, 44)
        slab.midbottom = (PLAY_W // 2, 790)
        for lx in (slab.x + 50, slab.x + 180, slab.right - 202, slab.right - 72):
            pygame.draw.rect(s, TABLE_EDGE, (lx, slab.y - 170, 22, 172), border_radius=4)
            pygame.draw.rect(s, (40, 24, 12), (lx - 4, slab.y - 182, 30, 16), border_radius=4)
        pygame.draw.rect(s, WOOD_DARK, slab, border_radius=10)
        pygame.draw.rect(s, FELT, slab.move(0, 30).clip(slab), border_radius=6)
        cw, ch = self.card_size
        back = pygame.Surface((cw + 4, ch + 5), pygame.SRCALPHA)
        render_card(back, None, (0, 0, cw, ch), False)
        for x, y, ang in self.floor_cards:
            img = pygame.transform.rotate(back, ang)
            s.blit(img, img.get_rect(center=(int(x), int(y))))
        blit_text(s, "GAME OVER", 96, GOLD, (PLAY_W // 2, 150), "center")
        blit_text(s, f"{self.name(self.flipper)} flipped the table.", 44, (255, 120, 110),
                  (PLAY_W // 2, 240), "center")
        blit_text(s, "Nobody wins.", 44, WHITE, (PLAY_W // 2, 292), "center")

    # ------------------------------------------------------------ main loop
    def play_game(self):
        """game_loop(): keep handling input and drawing until the window closes."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.now += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)
            self.update_effects(dt)
            self.render_game()
            pygame.display.flip()
        pygame.quit()


def main():
    CambioApp().play_game()
    sys.exit()


if __name__ == "__main__":
    main()
