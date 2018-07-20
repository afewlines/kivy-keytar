from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

# non kivy imports
from random import randint


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
    tiles = ['graphics/tile0.png',
             'graphics/tile1.png']
    keyBindings = {'a': 0, 's': 1, 'k': 2, 'l': 3}
    board = []
    screenTiles = [[], [], [], []]
    currentRow = 0
    ttime = 0

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.checkKey)

        self.orientation = 'vertical'
        self.grid = GridLayout(cols=4)
        self.header = BoxLayout(orientation='horizontal',
                                size_hint_max=(None, 30))

        self.timer = Label(text='EXAMPLE TIMER')
        self.header.add_widget(self.timer)
        self.level = Label(text=str(GameScreen.currentRow))
        self.header.add_widget(self.level)

        self.add_widget(self.header)
        self.add_widget(self.grid)

        GameScreen.board = Board(50).getBoard()
        self.updateScreen()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def updateScreen(self):
        for row in range(0, 4):
            GameScreen.screenTiles[row] = GameScreen.board[row +
                                                           GameScreen.currentRow]
        self.grid.clear_widgets()
        self.level.text = str(GameScreen.currentRow)
        for row in range(0, 4):
            for tile in range(0, 4):
                self.grid.add_widget(
                    Image(source=GameScreen.tiles[GameScreen.screenTiles[3 - row][tile]]))

    def checkKey(self, keyboard, keycode, text, modifiers):
        if keycode[1] in GameScreen.keyBindings:
            if GameScreen.board[GameScreen.currentRow][GameScreen.keyBindings[keycode[1]]] == 1:
                GameScreen.currentRow += 1
                print('haha N0ICE')
                self.updateScreen()
            else:
                self.fail()

    def fail(self):
        print('r i p my dude')
        self.grid.clear_widgets()


class KeytarApp(App):
    def build(self):
        return GameScreen()


if __name__ == '__main__':
    Config.set('graphics', 'borderless', '1')
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '630')
    Config.set('graphics', 'resizable', '0')
    Config.write()
    KeytarApp().run()
