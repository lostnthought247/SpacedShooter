from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import CoreLabel
from kivy.uix.screenmanager import Screen
from random import randint
from kivy.vector import Vector

from spacegame import PlayerShip


def collides(rect1, rect2):
    """Check for a collision between two rectangles."""
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][0]
    r1h = rect1[1][1]
    r2w = rect2[1][0]
    r2h = rect2[1][1]

    return r1x < r2x + r2w and \
        r1x + r1w > r2x and \
        r1y < r2y + r2h and \
        r1y + r1h > r2y


class IntroScreen(Screen):
    """The very first screen with options to start, continue, or quit."""
    pass


class BaseScreen(Screen):
    """The home base screen where a user selects the ship to use."""
    speed = StringProperty()
    hp = StringProperty()
    attack = StringProperty()
    ammo = StringProperty()
    skin = StringProperty()
    ship = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.select_ship('basic')

    def select_ship(self, type):
        """Change the stats of the ship on the base page."""
        ship = PlayerShip(shiptype=type)
        self.speed = str(ship.stats['speed'])
        self.hp = str(ship.stats['hp'])
        self.attack = str(ship.stats['attack'])
        self.ammo = str(ship.stats['ammo'])
        self.skin = ship.skin
        self.ship = ship



class CombatScreen(Screen):
    """The screen that the user flies around shooting enemies."""
    player = ObjectProperty(None)
    angle = NumericProperty(0)

    shiptype = StringProperty('fast')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.score_label = CoreLabel(text="Score: 0")
        self.score_label.refresh()

        # Create a set of pressed keys for the given moment
        self.keysPressed = set()

        # Set the event interval of every frame
        Clock.schedule_interval(self.move_hero, 1.0/60.0)

    def get_background(self):
        background = str("space" + str(randint(1,4)) + ".png")
        return background

    def on_enter(self):
        """Initialize the combat."""
        Logger.info('Combat is beginning in shiptype "{}"'.format(self.shiptype))
        # self.player = PlayerShip(self.shiptype)

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

    def move_hero(self, dt):
        """Move the player ship according to the key pressed."""
        for i in [0, 1]:
            if self.player.pos[i] < -5:
                self.player.pos[i] = Window.size[i]
            elif self.player.pos[i] > Window.size[i]+10:
                self.player.pos[i] = 0

        Logger.debug(self.player)
        x = self.player.pos[0]
        y = self.player.pos[1]
        a = self.player.angle
        rotation = 0
        velocity = self.player.velocity

        angle_delta = 1

        if "w" in self.keysPressed:
            # Logger.info('"w" was pressed.')
            if velocity < 13:
                velocity += 0.25

        if "s" in self.keysPressed:
            if velocity > 0:
                velocity -= 0.25
        if "a" in self.keysPressed:
            rotation += angle_delta
        if "d" in self.keysPressed:
            # Logger.info('"d" was pressed.')
            rotation -= angle_delta


        self.player.angle = a + rotation

        # if velocity > 0 : velocity -= 0.05
        self.player.velocity = velocity
        self.player.pos = Vector(self.player.velocity, 0).rotate(self.player.angle) + self.player.pos




    #
    # def move_hero(self, dt):
    #     """Move the player ship according to the key pressed."""
    #     Logger.debug(self.player)
    #     x = self.player.pos[0]
    #     y = self.player.pos[1]
    #     a = self.player.angle
    #
    #     current_velocity = 0
    #     delta = 1 * current_velocity
    #     angle_delta = 1
    #
    #     if "w" in self.keysPressed:
    #         # Logger.info('"w" was pressed.')
    #         y += delta
    #     if "s" in self.keysPressed:
    #         y -= delta
    #     if "a" in self.keysPressed:
    #         a += angle_delta
    #     if "d" in self.keysPressed:
    #         # Logger.info('"d" was pressed.')
    #         a -= angle_delta
    #     # Logger.info('The new position is ({}, {})'.format(x, y))
    #     self.player.pos = (x, y)
    #     self.player.angle = a





class ReturnScreen(Screen):
    """The screen displayed upon level completion before return to base."""
    pass

class Save_Load_Settings_Menu(Screen):
    """The menu for saving/loading or altering game settings"""
    pass


class SpaceGameApp(App):
    """The kivy application."""

    def build(self):
        """Build the app and return an app object that can be run."""
        presentation = Builder.load_file("app.kv")
        return presentation
