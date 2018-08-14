from tkinter import *
from tkinter import ttk
import os
from copy import deepcopy
import time
import random

class Field:
    def __init__(self, root_window, pos_x, pos_y, blank, circle, cross, parent):
        self.root = root_window
        self.x = pos_x
        self.y = pos_y
        
        self.parent = parent
        self.owner = None

        #to do obrazków muszą to być PhotoImage
        self.blank = blank
        self.circle = circle
        self.cross = cross

        self.label = Label(self.root, borderwidth = 2, background = 'black')
        self.label['image'] = blank
        self.label.grid(column = self.x, row = self.y)
        self.label.bind('<Button-1>', self.clicked)

    def unbind(self):
        self.label.unbind('<Button-1>')

    def clicked(self, event):
        if self.parent.player == 'player':
            self.unbind()
            self.label['image'] = self.cross
            self.root.update_idletasks()
            self.owner = 'player'
            self.parent.player_click(tuple(self))
            
    def __iter__(self):
        yield self.x
        yield self.y

    def computer_click(self):
        if self.parent.player == 'computer':
            self.unbind()
            self.owner = 'computer'
            self.label['image'] = self.circle

class Game:
    base_folder = os.path.dirname(__file__)
    def __init__(self):
        self.player = 'player'
        self.root = Tk()

        self.blank = PhotoImage(file=os.path.join(Game.base_folder, 'blank.gif'))
        self.circle = PhotoImage(file=os.path.join(Game.base_folder, 'circle.gif'))
        self.cross = PhotoImage(file=os.path.join(Game.base_folder, 'cross.gif'))

        self.root.geometry("200x100")
        self.root.title('Tic Tac Toe')

        self.info_label = Label(self.root, text='Tic Tac Toe')
        self.info_label.pack(side=TOP, pady = 10)
        self.start_button = ttk.Button(self.root, text='START')
        self.start_button.pack(side=BOTTOM, pady = 10)

        self.start_button.bind('<Button-1>', self.make_board)
        
        self.root.mainloop()

    def make_board(self, event):
        self.root.withdraw()
        self.game_frame = Toplevel()
        self.game_frame.protocol("WM_DELETE_WINDOW", self.close_game_frame)
        self.game_frame.title('Tic Tac Toe')
        self.start_game()

    def start_game(self):
        self.tiles = dict()
        for y in range(3):
            for x in range(3):
                self.tiles[(x, y)] = Field(self.game_frame, x, y, self.blank, self.circle, self.cross, self)
        
        self.av_tiles_pos = list(self.tiles.keys())
        self.player = 'player'
        # print(self.av_tiles_pos)

    def close_game_frame(self):
        self.game_frame.destroy()
        self.root.destroy()

    def player_click(self, who_clicked):
        try:
            self.av_tiles_pos.remove(who_clicked)
        except:
            pass
        # print(who_clicked, self.av_tiles_pos)
        self.player = 'computer'
        if not (self.check() == True):
            time.sleep(0.5)
            self.computer_turn()
        else:
            self.end_game()

    def computer_turn(self):
        try:
            computer_choice = random.choice(self.av_tiles_pos)
            self.av_tiles_pos.remove(computer_choice)
            self.tiles[computer_choice].computer_click()
            self.player = 'player'
        except:
            pass
        if self.check() == True:
            for elem in self.av_tiles_pos:
                self.tiles[elem].unbind()
            self.end_game()

    def check(self):
        if len(self.av_tiles_pos) >= 0:
            # vertical stripes
            # x00|x00|x00
            if self.tiles[(0,0)].owner == self.tiles[(0,1)].owner == self.tiles[(0,2)].owner:
                if self.tiles[(0,0)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(0,0)].owner == 'computer':
                    self.winner('computer')
                    return True
            # 0x0|0x0|0x0
            if self.tiles[(1,0)].owner == self.tiles[(1,1)].owner == self.tiles[(1,2)].owner:
                if self.tiles[(1,0)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(1,0)].owner == 'computer':
                    self.winner('computer')
                    return True
            # 00x|00x|00x
            if self.tiles[(2,0)].owner == self.tiles[(2,1)].owner == self.tiles[(2,2)].owner:
                if self.tiles[(2,0)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(2,0)].owner == 'computer':
                    self.winner('computer')
                    return True
            # horizontal stripes
            # xxx|000|000
            if self.tiles[(0,0)].owner == self.tiles[(1,0)].owner == self.tiles[(2,0)].owner:
                if self.tiles[(0,0)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(0,0)].owner == 'computer':
                    self.winner('computer')
                    return True
            # 000|xxx|000
            if self.tiles[(0,1)].owner == self.tiles[(1,1)].owner == self.tiles[(2,1)].owner:
                if self.tiles[(0,1)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(0,1)].owner == 'computer':
                    self.winner('computer')
                    return True
            # 000|000|xxx
            if self.tiles[(0,2)].owner == self.tiles[(1,2)].owner == self.tiles[(2,2)].owner:
                if self.tiles[(0,2)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(0,2)].owner == 'computer':
                    self.winner('computer')
                    return True
            # special stripes
            # x00|0x0|00x
            if self.tiles[(0,0)].owner == self.tiles[(1,1)].owner == self.tiles[(2,2)].owner:
                if self.tiles[(0,0)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(0,0)].owner == 'computer':
                    self.winner('computer')
                    return True
            # 00x|0x0|x00
            if self.tiles[(0,2)].owner == self.tiles[(1,1)].owner == self.tiles[(2,0)].owner:
                if self.tiles[(0,2)].owner == 'player':
                    self.winner('player')
                    return True
                elif self.tiles[(0,2)].owner == 'computer':
                    self.winner('computer')
                    return True
        
        if len(self.av_tiles_pos) == 0:
            self.winner('tie')
            return True
            
    def winner(self, winner):
        self.txt = ''
        if winner == 'player':
            self.txt = 'You won!'
        elif winner == 'computer':
            self.txt = 'Computer won!'
        elif winner == 'tie':
            self.txt = "It's a tie"
    
    def end_game(self):
        def onclose(event=None):
            self.popup.destroy()
            self.start_game()
              
        self.popup = Toplevel()
        self.popup.title('Game ends')
        self.popup.geometry("200x100")
        self.info_pop = Label(self.popup, text = self.txt)
        self.info_pop.pack(pady = 10)
        self.info_button = Button(self.popup, text='Okay')
        self.info_button.pack(side=BOTTOM, pady=10)
        self.popup.protocol("WM_DELETE_WINDOW", onclose)
        self.info_button.bind('<Button-1>', onclose)

if __name__ == '__main__':
    Game()