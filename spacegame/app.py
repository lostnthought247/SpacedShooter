"""Put all the pieces together to form the Spaced Out! application.

Run the application by importing the `SpaceGameApp` class and calling its
`run()` method. For example::

    from spacegame.app import SpaceGameApp
    SpaceGameApp().run()

"""
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import CoreLabel
from kivy.uix.screenmanager import Screen
from kivy.vector import Vector
from random import randint

from spacegame import PlayerShip


class IntroScreen(Screen):
    """The very first screen with options for changing screens.

    New Game - Go to the base screen to choose an initial ship.
    Continue - Go to the screen for loading saved games.
    Quit - Exit the application.

    """

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Intro screen.')


class BaseScreen(Screen):
    """The home base screen where a user selects the ship to use.

    From home base it is possible to go to other screens:

    Main Menu - Go back to the intro screen.
    Launch Mission - Go to the combat screen using the selected ship.

    """

    speed = StringProperty()
    hp = StringProperty()
    attack = StringProperty()
    ammo = StringProperty()
    skin = StringProperty()
    ship = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.select_ship('basic')

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Base screen.')
        Logger.info(
            'Application: '
            'The ship displayed in the base is the '
            '"{}" type.'.format(self.ship.type)
            )

    def select_ship(self, type):
        """Change the stats of the ship on the base page.

        Args:
            type (str): The type of ship to display the stats for.

        """
        ship = PlayerShip(shiptype=type)
        self.speed = str(ship.stats['speed'])
        self.hp = str(ship.stats['hp'])
        self.attack = str(ship.stats['attack'])
        self.ammo = str(ship.stats['ammo'])
        self.skin = ship.skin
        self.ship = ship
        Logger.info(
            'Application: '
            'Changing the ship displayed in the base to the '
            '"{}" type.'.format(self.ship.type)
            )


class CombatScreen(Screen):
    """The screen that the user flies around shooting enemies."""

    player = ObjectProperty(None)
    shiptype = StringProperty(None)
    updater = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.score_label = CoreLabel(text="Score: 0")
        self.score_label.refresh()

        # Create a set of pressed keys for the given moment
        self.keysPressed = set()

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Combat screen.')
        Logger.info(
            'Application: '
            'The ship chosen for combat is the '
            '"{}" type.'.format(self.player.type)
            )
        Logger.info('Application: Stats: {}.'.format(self.player.stats))

        # Set the event interval of every frame
        self.updater = Clock.schedule_interval(self.update, 1.0/60.0)

    def on_pre_leave(self):
        """Perform clean up right before the scene is switched from."""
        self.updater.cancel()  # Clear the event interval.

    def get_background(self):
        """Choose a random image for the scene's background."""
        return 'space{}.png'.format(randint(1, 4))

    def on_keyboard_closed(self):
        """Act on the keyboard closing."""
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard.unbind(on_key_up=self.on_key_up)
        self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        """Act on a key being pressed down."""
        self.keysPressed.add(text)

    def on_key_up(self, keyboard, keycode):
        """Act on a key being released up."""
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def accelerate_hero(
        self, maxspeed=13, minspeed=0, acceleration=0.25, turning=1
    ):
        """Calculate the acceleration changes based on the key pressed."""
        rotation = 0
        speed = self.player.speed

        if "w" in self.keysPressed:
            if speed < maxspeed:
                speed = min(maxspeed, speed + acceleration)
        if "s" in self.keysPressed:
            if speed > minspeed:
                speed = max(minspeed, speed - acceleration)
        if "a" in self.keysPressed:
            rotation += turning
        if "d" in self.keysPressed:
            rotation -= turning

        self.player.angle += rotation
        self.player.speed = speed

    def move_hero(self):
        """Advance the player ship position according to its velocity."""
        delta = Vector(self.player.speed, 0).rotate(self.player.angle)
        self.player.pos = delta + self.player.pos
        for i in [0, 1]:  # Wrap the screen.
            if self.player.pos[i] < -5:
                self.player.pos[i] = Window.size[i]
            elif self.player.pos[i] > Window.size[i]+10:
                self.player.pos[i] = 0

    def update(self, dt):
        """Step the scene forward."""
        self.accelerate_hero()
        self.move_hero()


class ReturnScreen(Screen):
    """The screen displayed upon level completion before return to base.

    Back To Menu - Go back to the intro screen.
    Settings - Go to the game settings screen.

    """

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Return screen.')


class SpaceGameApp(App):
    """The kivy application."""

    def build(self):
        """Build the app and return an app object that can be run."""
        Logger.info('Application: Kivy has finally finished loading.')
        Logger.info('Application: Building "Spaced Out!" so you can run it...')
        presentation = Builder.load_file("app.kv")
        Logger.info('Application: ...Built. Run it by calling `self.run()`.')
        return presentation
