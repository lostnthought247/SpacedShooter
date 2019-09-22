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

class IntroScreen(Screen):
    # A filler class-tool that is used and controled by game .ky file elsewhere
    pass

class BaseScreen(Screen):
    selected_ship = "ship1.png"
    ship_speed = 100
    ship_hp =  100
    ship_attack =  100

class CombatScreen(Screen):
    pass

class ReturnScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class PlayerShip(Widget):
    Speed = None
    HP = None
    Attack = None


    # sets velocity of the ship on x and y axis as .ky numeric properties
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ship.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)




# Creates the game instance and display/update controls
class SpaceGame(Widget):
        def update(self, dt):
            pass

        ## Sets background sound
        # self.sound=SoundLoader.load("music.wav")
        # self.sound.play()

# Initiates application window and features?
class SpaceGameApp(App):
    def build(self):
        # Loads and builds view based on SpaceGame.kv file
        presentation = Builder.load_file("SpaceGame.kv")
        game = SpaceGame()
        # Sets game update interval
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return presentation

    def update(self):
        pass

if __name__ == "__main__":
    SpaceGameApp().run()
