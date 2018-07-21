from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class Board():
    def __init__(self, arg):
        super(Board, self).__init__()
        self.arg = arg
        self.board = []
        for row in range(arg):
            temprow = [0, 0, 0, 0]
            temprow[randint(0, 3)] = 1
            self.board.append(temprow)
        for row in range(4):
            temprow = [0, 0, 0, 0]
            self.board.append(temprow)

    def getBoard(self):
        return self.board


class GameScreen(BoxLayout):
    active = False
    tiles = ['graphics/tile0.png',
             'graphics/tile1.png']
    key_binds = {'a': 0, 's': 1, 'k': 2, 'l': 3}
    board = []
    screen_tiles = [[], [], [], []]
    current_row = 0
    ttime = 0
    start_timer = False

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keypress)

        self.orientation = 'vertical'
        self.grid = GridLayout(cols=4)
        self.header = BoxLayout(orientation='horizontal',
                                size_hint_max_y=30)

        self._scrWin = Label(text='EXAMPLE TIMER',
                             font_size=24, size_hint_max_y=400, halign='center')
        self._scrReset = Label(
            text='press \'r\' or \'spacebar\' to start', font_size=24, size_hint_max_y=400, halign='center')
        self._scrCurrent = self._scrReset

        self.timer_label = Label(
            text=str(GameScreen.ttime), text_size=(150, None))
        self.header.add_widget(self.timer_label)
        self.level = Label(text=str(GameScreen.current_row),
                           text_size=(150, None), halign='right')
        self.header.add_widget(self.level)

        self.add_widget(self.header)
        # self.add_widget(self.grid)

        self.add_widget(self._scrReset)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keypress)
        self._keyboard = None

    def _on_keypress(self, keyboard, keycode, text, modifiers):
        if not GameScreen.active:
            if keycode[1] in ['r', 'spacebar']:
                self.reset()
            return

        if GameScreen.start_timer:
            Clock.schedule_interval(self.timer, 0.01)
            GameScreen.start_timer = False

        if keycode[1] in GameScreen.key_binds:
            if GameScreen.board[GameScreen.current_row][GameScreen.key_binds[keycode[1]]] == 1:
                GameScreen.current_row += 1
                self.update_screen()
            else:
                self.fail()

    def timer(self, dt):
        if GameScreen.active:
            GameScreen.ttime += dt
            self.timer_label.text = '{0:.3f}'.format(GameScreen.ttime)
        else:
            return False

    def update_screen(self):
        self.level.text = str(GameScreen.current_row)
        if GameScreen.current_row >= 50:
            self.win()
            return
        for row in range(0, 4):
            GameScreen.screen_tiles[row] = GameScreen.board[row +
                                                            GameScreen.current_row]
        self.grid.clear_widgets()
        for row in range(0, 4):
            for tile in range(0, 4):
                self.grid.add_widget(
                    Image(source=GameScreen.tiles[GameScreen.screen_tiles[3 - row][tile]]))

    def fail(self):
        GameScreen.active = False
        self.grid.clear_widgets()
        self.remove_widget(self.grid)
        self._scrReset.text = "you lost :(\npress 'r' or 'spacebar' to restart"
        self._scrCurrent = self._scrReset
        self.add_widget(self._scrCurrent)

    def win(self):
        GameScreen.active = False
        self.grid.clear_widgets()
        self.remove_widget(self.grid)
        self._scrWin.text = "you won!\ntime: {}\npress 'r' or 'spacebar' to restart".format(
            self.timer_label.text)
        self._scrCurrent = self._scrWin
        self.add_widget(self._scrCurrent)

    def reset(self):
        GameScreen.active = True
        GameScreen.start_timer = True
        GameScreen.current_row = 0
        GameScreen.ttime = 0
        GameScreen.board = Board(50).getBoard()
        self.remove_widget(self._scrCurrent)
        self.add_widget(self.grid)
        self.update_screen()


class KeytarApp(App):
    def build(self):
        return GameScreen()


if __name__ == '__main__':
    # Config.set('graphics', 'borderless', '1')
    # Config.set('graphics', 'width', '400')
    # Config.set('graphics', 'height', '630')
    # Config.set('graphics', 'resizable', '0')
    # Config.write()
    KeytarApp().run()
