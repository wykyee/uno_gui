class Player:

    def __init__(self, hand, player_id):
        self.hand = hand
        self.player_id = player_id

    def can_play(self, prev_card):
        for card in self.hand:
            if card.playable(prev_card):
                return True
        return False

    def choose_card(self, prev_card):
        self.waiting_for_player = self.can_play(prev_card)
        return None

    def pick_card(self, deck, num_cards):
        cards = [deck.pop(0) for _ in range(num_cards)]
        self.hand.extend(cards)

        return

    def put(self, card, deck):
        card_ind = self.hand.index(card)
        put_card = self.hand.pop(card_ind)
        deck.append(put_card)

        return

    def __repr__(self):
        return f'Player {self.player_id} Object, hand: {self.hand}'

    def __str__(self):
        return f'ID: {self.player_id}, hand: {self.hand}'


class Bot(Player):

    def choose_card(self, prev_card):
        self.waiting_for_player = False
        if self.can_play(prev_card):
            chosen_card = None

            i = 0
            while chosen_card is None:
                if self.hand[i].playable(prev_card):
                    chosen_card = self.hand[i]
                i += 1
        else:
            chosen_card = None

        return chosen_card

    def __repr__(self):
        return f'Bot {self.player_id} Object, hand {self.hand}'
