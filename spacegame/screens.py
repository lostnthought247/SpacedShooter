from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.label import CoreLabel
from kivy.uix.screenmanager import Screen
from random import choice

from spacegame.entities.ships import PlayerShip
from spacegame.config import physics
from spacegame.config import screens
from spacegame.managers import SoundManager
from random import randint


class IntroScreen(Screen):
    """The very first screen with options for changing screens.

    New Game - Go to the base screen to choose an initial ship.
    Continue - Go to the screen for loading saved games.
    Quit - Exit the application.

    """
    source = None

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Intro screen.')
        self.start_soundtrack()

    def on_pre_leave(self):
        """Clean up the scene."""
        Logger.info('Application: Leaving the Intro screen.')

    def start_soundtrack(self):
        """Choose and play music for the intro scene."""
        sources = screens['Intro']['music']
        self.source = choice(sources)
        Logger.info('Chose "{}" as the intro music.'.format(self.source))
        try:
            SoundManager.music[self.source]
        except KeyError:
            SoundManager.add_music(self.source, self)
            SoundManager.play_music(self.source)

    def stop_soundtrack(self):
        """Stop the intro scene music."""
        SoundManager.remove_music(self.source, self)


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
    source = None

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

    def on_pre_leave(self):
        """Clean up the scene."""
        Logger.info('Application: Leaving the Intro screen.')

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
    hostile = ObjectProperty(None)
    shiptype = StringProperty(None)
    updater = None
    lives = NumericProperty(None)


    # In progress 10/7 - sets kv list prop. for ships, objects, and explosions
    spaceships = ListProperty()
    asteroids = ListProperty()
    explosions = ListProperty()
    hostile_odd_move = True
    random_select_action = None


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
        self.start_soundtrack()

        # Set the event interval of every frame
        self.updater = Clock.schedule_interval(self.update, 1.0/60.0)

    def on_pre_leave(self):
        """Perform clean up right before the scene is switched from."""
        Logger.info('Application: Leaving the Combat screen.')
        self.updater.cancel()  # Clear the event interval.
        self.stop_soundtrack()

    def on_keyboard_closed(self):
        """Act on the keyboard closing."""
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard.unbind(on_key_up=self.on_key_up)
        self.keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        """Act on a key being pressed down."""
        Logger.debug('KeyDown Event: Keycode[1] is "{}"'.format(keycode[1]))
        self.keysPressed.add(keycode[1])

    def on_key_up(self, keyboard, keycode):
        """Act on a key being released up."""
        Logger.debug('KeyUp Event: Keycode[1] is "{}"'.format(keycode[1]))
        self.keysPressed.remove(keycode[1])

    def accelerate_hero(
        self, unit, physics=physics
    ):
        """Calculate the acceleration changes based on the key pressed."""
        minspeed = 0
        rotation = 0
        speed = self.player.speed
        topspeed = self.player.stat('speed')

        # Acceleration and turning are configs that modify movement overall.
        acceleration = physics.get('acceleration', 0.25)
        turning = physics.get('turning', 25)

        # Make rotation dependent on speed.
        angle_delta = turning * unit * topspeed
        # Make acceleration dependent on speed.
        speed_delta = acceleration * unit * topspeed

        if "w" in self.keysPressed:
            if speed < topspeed:
                speed = min(topspeed, speed + speed_delta)
        if "s" in self.keysPressed:
            if speed > minspeed:
                speed = max(minspeed, speed - speed_delta)
        if "a" in self.keysPressed:
            rotation += angle_delta
        if "d" in self.keysPressed:
            rotation -= angle_delta
        if "spacebar" in self.keysPressed:
            self.player.fire()

        self.player.angle += rotation
        self.player.speed = speed

    def accelerate_hostile(
        self, unit, physics=physics
    ):
        """Calculate the acceleration changes based on the key pressed."""
        minspeed = 0
        rotation = 0
        speed = self.hostile.speed
        topspeed = self.hostile.stat('speed')

        # Acceleration and turning are configs that modify movement overall.
        acceleration = physics.get('acceleration', 0.25)
        turning = physics.get('turning', 25)

        # Make rotation dependent on speed.
        angle_delta = turning * unit * topspeed
        # Make acceleration dependent on speed.
        speed_delta = acceleration * unit * topspeed


        random_select_action = randint(1,5)

        if random_select_action == 1:
            if speed < topspeed:
                speed = min(topspeed, speed + speed_delta*4)
        if random_select_action == 2:
            if speed > minspeed:
                speed = max(minspeed, speed - speed_delta*4)
        if random_select_action == 3:
            rotation += angle_delta
        if random_select_action == 4:
            rotation -= angle_delta
        # if random_select_action == 5:
        #     self.hostile.fire()

        self.hostile.angle += rotation
        self.hostile.speed = speed

    def update(self, dt):
        """Step the scene forward."""
        # First, step time forward.
        self.player.lastfired += dt
        self.accelerate_hero(dt)
        self.accelerate_hostile(dt)

        # Next, move the objects around the screen
        self.player.move(windowsize=Window.size)
        self.hostile.move(windowsize=Window.size)
        for shell in self.player.shells:
            shell.move(windowsize=Window.size)
            if shell.offscreen:
                self.player.shells.remove(shell)
                self.remove_widget(shell)

        # Finally, check for any collisions
        self.detect_collisions()

    def new_remove_widget(self, widget_object):
        self.ids.GameView.remove_widget(widget_object)

    def detect_collisions(self):
        if self.player.collide_widget(self.hostile):
            #
            #sfx = SoundManager.sfx.get("explosion1.ogg")
            #SoundManager.play_sfx("explosion1.ogg")
            Logger.info("Ship 2 Ship Collision Detected!")
            #self.hostile.pos = (-10000, -10000)
            self.new_remove_widget(self.hostile)
            self.new_remove_widget(self.player)
        for shell in self.player.shells:
            if self.hostile.collide_widget(shell):
             Logger.info("Ship 2 Shot Collision Detected!")
             self.new_remove_widget(self.hostile)
        #     sssself.hostile.pos = (-10000, -10000)
        #     self.player.shells.pos = (-10000, -10000)

    def start_soundtrack(self):
        """Choose and play music for the combat scene."""
        sources = screens['Combat']['music']
        self.source = choice(sources)
        Logger.info('Chose "{}" as the combat music.'.format(self.source))
        try:
            SoundManager.music[self.source]
        except KeyError:
            SoundManager.add_music(self.source, self)
            SoundManager.play_music(self.source)

    def stop_soundtrack(self):
        """Stop the combat scene music."""
        SoundManager.remove_music(self.source, self)


class ReturnScreen(Screen):
    """The screen displayed upon level completion before return to base.

    Back To Menu - Go back to the intro screen.
    Settings - Go to the game settings screen.

    """

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Return screen.')


class SettingsScreen(Screen):
    """The screen for changing game settings.

    Back To Menu - Go back to the intro screen.

    """

    def on_pre_enter(self):
        """Perform tasks to ready the scene right before it is switched to."""
        Logger.info('Application: Changed to the Settings screen.')
