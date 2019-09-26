from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import CoreLabel
from random import randint
from random import choice

def collides(rect1, rect2):
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][0]
    r1h = rect1[1][1]
    r2w = rect2[1][0]
    r2h = rect2[1][1]

    if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    else:
        return False

# Creates the player ship object used by .kv and .py code
class PlayerShip(Widget):
    Speed = None
    HP = None
    Attack = None

    def move_player(self):
        newX = self.pos[0] + 10
        newY = self.pos[1] + 10
        self.pos = (newX, newY)


# Creates a screen obj. used by kivy in kv file
class IntroScreen(Screen):
    pass

# Creates a screen obj. used by kivy in kv file. Defines some temp display vars
class BaseScreen(Screen):
    selected_ship = "ship1.png"
    ship_speed = 100
    ship_hp =  100
    ship_attack =  100

# Creates a screen obj. used by kivy in kv file
class CombatScreen(Screen):
    player = PlayerShip()
    player.move_player()

    def move_player(self):
        newX = player.pos[0] + 10
        newY = player.pos[1] + 10
        player.pos = (newX, newY)

    pass

# Creates a screen obj. used by kivy in kv file
class ReturnScreen(Screen):
    pass

# Creates the screen manager obj. used by kivy in kv file
class ScreenManagement(ScreenManager):
    pass


# Game Widget
class SpaceGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.score_label = CoreLabel(text="Score: 0")
        self.score_label.refresh()

        with self.canvas:
            self.player = Rectangle(source = "Hero.png", pos=(0,0), size=(Window.width/4,Window.height/4))
            if self.player.pos[0] > Window.width:
                self.player.pos[0] = Window.width
            elif self.player.pos[0] < 0:
                self.player.pos[0] = 0
            if self.player.pos[1] > Window.height:
                self.player.pos[1] = Window.height
            elif self.player.pos[1] < 0:
                self.player.pos[1] = 0

            relative_x = self.player.pos[0] / Window.width
            relative_y = self.player.pos[1] / Window.height
            self.player.pos = (relative_x, relative_y)
            # hostileNum = randint(1,3)
            # self.hostile =  Rectangle(source = str("Monster" + str(hostileNum) + ".png"), pos=(500,500), size=(Window.width/4,Window.height/4))
            self.score_instruction = Rectangle(texture = self.score_label.texture, pos=(0,Window.height-50), size=self.score_label.texture.size)
        # creates a set of pressed keys in for the given moment
        self.keysPressed = set()

        # sets and event interval of every frame
        Clock.schedule_interval(self.move_hero,0)
        # Clock.schedule_interval(self.move_hostile,0)

        ## Sets background sound
        # self.sound=SoundLoader.load("music.wav")
        # self.sound.play()



    def on_keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard.unbind(on_key_up=self.on_key_up)
        self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)

    def on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_hero(self, dt):
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 200 * dt

        if "w" in self.keysPressed:
            currenty += step_size
        if "s" in self.keysPressed:
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size
        self.player.pos = (currentx, currenty)

    # def move_hostile(self, dt):
    #     # Names hostiles x/y coordinates
    #     hostile_x = self.hostile.pos[0]
    #     hostile_y = self.hostile.pos[1]
    #
    #     # rolls for "smart" move or not
    #     roll = randint(1,10)
    #     if roll % 2 == 0:
    #     # Permorms "Smart move" moving x and y towards hero
    #         # Note: ' *dt ' call multiplies by "delta time" to equalize
    #         # movement speed accross differing framerate performance
    #         if self.player.pos[0] > self.hostile.pos[0]:
    #             new_hostile_step_x = hostile_x + 200 * dt
    #         else:
    #             new_hostile_step_x = hostile_x - 200 * dt
    #
    #         if self.player.pos[1] > self.hostile.pos[1]:
    #             new_hostile_step_y = hostile_y + 200 * dt
    #         else:
    #             new_hostile_step_y = hostile_y - 200 * dt
    #     else:
    #         # Permorms Random move - altering x and y wihtout pattern
    #         x_move_options = [-200, 0, 200]
    #         y_move_options = [-200, 0, 200]
    #         new_hostile_step_x = hostile_x + (choice(x_move_options) * dt)
    #         new_hostile_step_y = hostile_y + (choice(y_move_options) * dt)
    #     self.hostile.pos = (new_hostile_step_x, new_hostile_step_y)

# Game App
class SpaceGameApp(App):
    def build(self):
        # Loads and builds view based on SpaceGame.kv file
        presentation = Builder.load_file("SpaceGame.kv")
        #game = SpaceGame()
        # Sets game update interval
        #Clock.schedule_interval(game.update, 1.0 / 60.0)
        return presentation


if __name__ == "__main__":
    SpaceGameApp().run()
