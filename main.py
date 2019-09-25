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
    pass

# Creates a screen obj. used by kivy in kv file
class ReturnScreen(Screen):
    pass

# Creates the screen manager obj. used by kivy in kv file
class ScreenManagement(ScreenManager):
    pass

# Creates the player ship object used by .kv and .py code
class PlayerShip(Widget):
    Speed = None
    HP = None
    Attack = None

    def move_player(self):
        newX = self.pos[0] + 10
        newY = self.pos[1] + 10
        self.pos = (newX, newY)


# Game Widget to update game
class SpaceGame(Widget):
        def update(self, dt):
            self.player.move_player()

# Game App to build window and set event update timer
class SpaceGameApp(App):
    def build(self):
        # Loads and builds view based on SpaceGame.kv file
        GameView = Builder.load_file("SpaceGame.kv")
        # Creates instance of game widget
        game = SpaceGame()
        # Sets game update interval
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        # Returns visual display is game based on .kv file
        return GameView


if __name__ == "__main__":
    SpaceGameApp().run()
