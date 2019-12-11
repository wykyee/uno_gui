import random
from tkinter import simpledialog

COLORS = ['red', 'yellow', 'blue', 'green']
NUMS = [str(i) for i in range(10)] + [str(i) for i in range(1, 10)]
WILD = ['skip', '+2', 'reverse']
CARD_TYPES = NUMS + WILD * 2
BL_WILD = ['+4', 'choose_color', 'choose_card_type', 'one_more_turn']


class CardError(Exception):
    message = 'Something wrong with your card'


class Card:

    def __init__(self, color, card_type):
        self.__validate(color, card_type)
        self.color = color
        self.card_type = card_type

    def playable(self, prev):
        if self.card_type == prev.card_type or self.color == prev.color:
            return True
        elif prev.color == 'black' or self.color == 'black':
            return True
        else:
            return False

    def play(self, turn_cycle, players):
        return self

    @staticmethod
    def __validate(color, card_type):
        if color in COLORS or color == 'black':
            if color in COLORS:
                if card_type not in CARD_TYPES:
                    raise CardError
            else:
                if card_type not in BL_WILD:
                    raise CardError
        else:
            raise CardError

        return

    def __repr__(self):
        return f'Card({self.color}, {self.card_type})'

    def __str__(self):
        return repr(self)


class SkipCard(Card):

    def play(self, turn_cycle, players):
        next(turn_cycle)

        return self


class ReverseCard(Card):

    def play(self, turn_cycle, players):
        turn_cycle.reverse()

        return self


class PickCard(Card):

    def play(self, turn_cycle, players=None):
        next(turn_cycle)

        return self


class ChooseColorCard(Card):

    def play(self, turn_cycle, players):
        cur_player = players[turn_cycle.position]
        if cur_player.__class__.__name__ == 'Bot':
            self.color = random.choice(COLORS)
        else:
            self.color = self.__ask_color()

        return self

    @staticmethod
    def __ask_color():
        nxt_clr = None
        while nxt_clr not in COLORS:
            nxt_clr = simpledialog.askstring("input", "choose color")
        return nxt_clr


class OneMoreTurnCard(Card):
    """
    Black card, gives possibility to put card 1 more time
    """
    def play(self, turn_cycle, players):
        for _ in range(len(players) - 1):
            next(turn_cycle)

        return self
