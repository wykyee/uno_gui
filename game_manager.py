from cards import *
from player import *
from turn_cycle import *
from tkinter import messagebox


class GameError(Exception):
    message = 'Something with your game settings'


class GameManager:

    def __init__(self, num_players, num_bots):
        self._winner = None
        self.deck = self.__create_deck()
        self.players = [
            Player(self.__create_hand(), i) for i in range(1, num_players + 1)
        ] + [
            Bot(self.__create_hand(), j)
            for j in range(num_players + 1, num_bots + num_players + 1)
        ]
        self.turn_cycle = TurnIterator(self.players)
        self.current_player = next(self.turn_cycle)

    @staticmethod
    def __create_deck():
        deck = []
        num_cards = [Card(clr, ct)
                     for clr in COLORS
                     for ct in NUMS]
        reverse_cards = [ReverseCard(clr, ct)
                         for clr in COLORS
                         for ct in ['reverse'] * 2]
        skip_cards = [SkipCard(clr, ct) for clr in COLORS for ct in ['skip']*2]
        pick2_cards = [PickCard(clr, ct)
                       for clr in COLORS
                       for ct in ['+2'] * 2]
        pick4_cards = [PickCard(clr, ct)
                       for clr in ['black'] * 4
                       for ct in ['+4']]
        choose_color_cards = [ChooseColorCard(clr, ct)
                              for clr in ['black'] * 4
                              for ct in ['choose_color']]
        one_more_turn_card = [OneMoreTurnCard(clr, ct)
                              for clr in ['black'] * 4
                              for ct in ['one_more_turn']]
        deck.extend(num_cards)
        deck.extend(reverse_cards)
        deck.extend(skip_cards)
        deck.extend(pick2_cards)
        deck.extend(pick4_cards)
        deck.extend(choose_color_cards)
        deck.extend(one_more_turn_card)

        random.shuffle(deck)
        return deck

    def __create_hand(self):
        return [self.deck.pop() for _ in range(7)]

    def top_card(self):
        return self.deck[-1]

    def game(self, player_input):
        top_card = self.top_card()
        cur_player = self.current_player

        cur_card = cur_player.choose_card(top_card)

        self.waiting_for_player = cur_player.waiting_for_player
        if self.waiting_for_player:
            if player_input is not None:
                if player_input < 0 or player_input >= len(cur_player.hand):
                    return
                cur_card = cur_player.hand[player_input]
                if not cur_card.playable(top_card):
                    return
                self.waiting_for_player = False
            else:
                return

        if cur_card is None:
            cur_player.pick_card(self.deck, 1)
            if not isinstance(cur_player, Bot):
                messagebox.showinfo('Winner',
                                    f"You don't have playable card")
            return

        elif isinstance(cur_card, PickCard):
            cur_player.put(cur_card.play(self.turn_cycle),
                           self.deck)
            self.players[self.turn_cycle.position].pick_card(
                self.deck, int(cur_card.card_type[1])
            )
            return

        else:
            cur_player.put(cur_card.play(self.turn_cycle, self.players),
                           self.deck)

        if self.__is_winner(cur_player):
            messagebox.showinfo('Winner',
                                f'Our winner is {cur_player.player_id}')

        return

    def __is_winner(self, player):
        if len(player.hand) < 1:
            self._winner = player.player_id
            return True

        return False

    def __next__(self):
        self.current_player = next(self.turn_cycle)
