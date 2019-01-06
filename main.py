from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import (CardTransition, Screen, ScreenManager,
                                    SlideTransition)

from encrypt import Encryptor

# CLASSES


class BoardGenerator():
    def __init__(self):
        self.boards = []
        self.current = -1

    def new_board(self, length):
        board = []
        for row in range(length):
            temprow = [0, 0, 0, 0]
            temprow[randint(0, 3)] = 1
            board.append(temprow)
        for row in range(4):
            temprow = [0, 0, 0, 0]
            board.append(temprow)
        self.boards.append(board)
        self.current += 1

    def get_board(self):
        if self.current >= 0:
            return self.boards[self.current]


# KIVY CLASSES

class BackgroundTile(BoxLayout):
    def __init__(self, bcolor=[1, 0, 0, 1], **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.bcolor = bcolor

# KIVY SCREENS


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.board = []
        self.generator = BoardGenerator()
        self.goal_row = 50
        self.current_row = 0
        self.ttime = 0
        self.start_timer = True
        self.grid = self.ids.grid
        self.active = False

    def reset(self):
        # put vars back to intial status
        self.board = []
        self.current_row = 0
        self.ttime = 0
        self.start_timer = True

    def update(self):
        # update grid
        self.grid.clear_widgets()
        for row in range(0, 4):
            for tile in range(0, 4):
                t = 1 - self.board[self.current_row + 3 - row][tile]
                self.grid.add_widget(BackgroundTile(bcolor=[t, t, t, 1]))

        # process win
        if self.current_row >= self.goal_row:
            self.active = False
            Player.SCREENS['win'].ids.time.text = "time: {}".format(
                self.ids.time.text)
            Player.change_screen('win')
            return

    def timer(self, dt):
        if self.active:
            self.ttime += dt
            self.ids.time.text = '{0:.3f}'.format(self.ttime)
        else:
            return False

    def on_pre_enter(self):
        self.generator.new_board(self.goal_row)
        self.board = self.generator.get_board()
        self.update()

    def on_leave(self):
        self.reset()

    def _on_keypress(self, keyboard, keycode, text, modifiers):
        if self.start_timer:
            self.active = True
            Clock.schedule_interval(self.timer, 0.01)
            self.start_timer = False

        if keycode[1] in Player.KEYS:
            if self.board[self.current_row][Player.KEYS[keycode[1]]] == 1:
                self.current_row += 1
                self.ids.level.text = '{}'.format(self.current_row)
                self.update()
            else:
                self.active = False
                Player.SCREENS['lose'].ids.level.text = "rows: {}".format(
                    self.current_row)
                Player.change_screen('lose')


class StartScreen(Screen):
    def on_enter(self):
        pass

    def _on_keypress(self, keyboard, keycode, text, modifiers):
        Player.change_screen('game')


class WinScreen(Screen):
    def on_enter(self):
        t_file = open(Player.L_FILE, 'a')
        t_file.write(Player.E.encrypt(self.ids.time.text[6:] + '\n'))
        t_file.close()
        Player.LEADERBOARD.append(self.ids.time.text[6:])
        Player.LEADERBOARD.sort()
        try:
            self.ids.l1.text = Player.LEADERBOARD[0]
            self.ids.l2.text = Player.LEADERBOARD[1]
            self.ids.l3.text = Player.LEADERBOARD[2]
            self.ids.l4.text = Player.LEADERBOARD[3]
            self.ids.l5.text = Player.LEADERBOARD[4]
        except:
            pass

    def _on_keypress(self, keyboard, keycode, text, modifiers):
        Player.change_screen('game')


class LoseScreen(Screen):
    def on_enter(self):
        pass

    def _on_keypress(self, keyboard, keycode, text, modifiers):
        Player.change_screen('game')


# KIVY INNARDS

class Player:
    MANAGER = ScreenManager()
    E = Encryptor()
    SCREENS = None
    LEADERBOARD = []
    L_FILE = 'o.txt'
    KEYS = {'a': 0, 's': 1, 'k': 2, 'l': 3}
    KEY = []
    ALPHA = [lt for lt in 'abcdefghijklmnopqrswxyz1234567890 ']

    def __init__(self):
        Player.SCREENS = {'start': StartScreen(name='start'),
                          'game': GameScreen(name='game'),
                          'win': WinScreen(name='win'),
                          'lose': LoseScreen(name='lose')}
        for scr in Player.SCREENS:
            Player.MANAGER.add_widget(Player.SCREENS[scr])

        Player.LEADERBOARD = Player.E.file_decrypt(Player.L_FILE)
        print(Player.LEADERBOARD)

        Player.change_screen('start')
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keypress)

    def _on_keypress(self, keyboard, keycode, text, modifiers):
        if Player.MANAGER.current_screen.transition_progress % 1 == 0:
            Player.MANAGER.current_screen._on_keypress(
                keyboard, keycode, text, modifiers)

    def _keyboard_closed(self):
        try:
            self._keyboard.unbind(on_key_down=self._on_keypress)
            self._keyboard = None
        except:
            pass

    def change_screen(target, *args, t=None):
        if t:
            Player.MANAGER.transition = t
        else:
            Player.MANAGER.transition = SlideTransition()

        try:
            Player.MANAGER.current = target
        except:
            print('   ERROR   Screen does not exist')


class KeytarApp(App):
    def build(self):
        sm = Player()
        return sm.MANAGER


if __name__ == '__main__':
    Config.set('graphics', 'borderless', '0')
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '630')
    Config.set('graphics', 'resizable', '1')
    Config.write()
    KeytarApp().run()
