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

# Initiates application window and features?


# Creates a screen obj. used by kivy in kv file
class IntroScreen(Screen):
    pass

# Creates a screen obj. used by kivy in kv file
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

class PlayerShip(Widget):
    Speed = None
    HP = None
    Attack = None

    def move_player(self):
        newX = self.pos[0] + 10
        newY = self.pos[1] + 10
        self.pos = (newX, newY)


# Game Widget
class SpaceGame(Widget):
        def update(self, dt):
            self.player.move_player()

# Game App
class SpaceGameApp(App):
    def build(self):
        # Loads and builds view based on SpaceGame.kv file
        presentation = Builder.load_file("SpaceGame.kv")
        game = SpaceGame()
        # Sets game update interval
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return presentation


if __name__ == "__main__":
    SpaceGameApp().run()
