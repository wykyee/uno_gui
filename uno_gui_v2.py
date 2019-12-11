from tkinter import *
from PIL import Image, ImageTk
from uno import *


class GameFrame(Frame):
    def __init__(self, game, master=None):
        Frame.__init__(self, master)
        self.game = game
        self.pack(fill=BOTH, expand=1)
        self.player_input = None

        self.draw_top_card()
        self.draw_deck_len()
        self.draw_hand_people()
        self.draw_hand_bots()

    def draw_top_card(self):
        tc_label = Label(self, text='Top card:', font='Arial 32', pady=30)
        tc_label.place(x=0, y=0)
        tc = self.game.top_card()
        if tc.color != 'black':
            load = Image.open(
                f'images/{tc.color[0]}_{tc.card_type}.png'
            )
        else:
            load = Image.open(
                f'images/{tc.color[0:2]}_{tc.card_type}.png'
            )
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=200, y=0)

    def draw_deck_len(self):
        deck_label = Label(self, text=f'Deck: {len(self.game.deck)}',
                           font='Arial 32', pady=30)
        deck_label.place(x=960, y=0)
        for i in range(1, 4):
            load = Image.open('images/wrap.png')
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=1130+i*20, y=0)

    def draw_hand_people(self):
        player = self.game.players[0]
        Label(
            self, text='1: ', font='Arial 40', pady=26, padx=20
        ).place(x=0, y=120)
        btn = []
        for i in range(len(player.hand)):
            Label(self, text=f'{i}', font='Arial 14').place(
                x=108 + i * 80, y=100
            )
            if player.hand[i].color != 'black':
                title = Image.open(
                    f'images/{player.hand[i].color[0]}_'
                    f'{player.hand[i].card_type}.png'
                )
            else:
                title = Image.open(
                    f'images/{player.hand[i].color[0:2]}_'
                    f'{player.hand[i].card_type}.png'
                )
            render = ImageTk.PhotoImage(title)
            btn.append(Button(image=render, command=lambda c=i: self.on_click(c), bd=0))
            btn[i].image = render
            btn[i].place(x=108+i*80, y=120)

    def on_click(self, indx):
        self.player_input = indx

    def draw_hand_bots(self):
        for bot in self.game.players[1:]:
            player_id_label = Label(self,
                                    text=str(bot.player_id)+': ',
                                    font='Arial 40', pady=26, padx=20
                                    )
            player_id_label.place(x=0, y=bot.player_id*120)
            for i, card in enumerate(bot.hand):
                wrap = Image.open('images/wrap.png')
                render = ImageTk.PhotoImage(wrap)
                img = Label(self, image=render)
                img.image = render
                img.place(x=108+i*80, y=bot.player_id*120)


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.game = GameManager(1, 3)
        self.pack(fill=BOTH, expand=1)

        self.gameFrame = GameFrame(self.game, self)
        self.update()

    def update(self):
        self.game.game(None)
        if self.game.waiting_for_player:
            if self.gameFrame.player_input is not None:
                self.game.game(self.gameFrame.player_input)
                self.gameFrame.player_input = None
                if self.game.waiting_for_player:
                    self.after(1000, self.update)
                    return
                next(self.game)
                self.gameFrame.destroy()
                self.gameFrame = GameFrame(self.game, self)
        else:
            next(self.game)
            self.gameFrame.destroy()
            self.gameFrame = GameFrame(self.game, self)

        if self.game._winner is None:
            self.after(1000, self.update)
        else:
            root.destroy()


root = Tk()
app = Window(root)
root.geometry('1280x720')
root.wm_title('UNO')
root.mainloop()
