from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.label import CoreLabel
from kivy.uix.screenmanager import Screen
from random import choice

from spacegame.entities.ships import PlayerShip
from spacegame.entities.objects import AsteroidObj
from spacegame.config import physics
from spacegame.config import screens
from spacegame.managers import SoundManager
from random import randint
from kivy.vector import Vector


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
    #asteroid = ObjectProperty(None)   # trash???
    shiptype = StringProperty(None)
    updater = None
    lives = NumericProperty(None)
    new_round = True


    # In progress 10/12 - sets kv list prop. for ships, objects, and explosions
    spaceships = []
    spaceships.append(player)
    spaceships.append(hostile)
    objects = []
    shells = []
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
        self.collidables = []
        self.spaceships = []
        self.spaceships.append(self.player)
        self.spaceships.append(self.hostile)
        for i in range(4):
            self.generate_asteroid()
        for asteroid in self.asteroids:
            self.collidables.append(asteroid)
            print("----------", self.collidables)
        for ship in self.spaceships:
            self.collidables.append(ship)

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


        random_select_action = randint(1,100)
        if random_select_action < 20:
            rotation += angle_delta
        elif random_select_action  < 40:
            rotation -= angle_delta
        elif random_select_action < 80:
            if speed < topspeed:
                speed = min(topspeed, speed + speed_delta)
        elif random_select_action < 90:
            if speed > minspeed:
                speed = max(minspeed, speed - speed_delta)

        if random_select_action == 20:
            self.hostile.fire()

        self.hostile.angle += rotation
        self.hostile.speed = speed

    # def set_asteroid_details(self):
    #     for asteroid in self.asteroids:
    #         if self.asteroid.angle == None:
    #             self.asteroid.angle =  randint(-360-360)
    #     self.asteroid.speed = 1

    def update(self, dt):
        """Step the scene forward."""
        # First, step time forward.
        self.player.lastfired += dt
        self.hostile.lastfired += dt
        self.accelerate_hero(dt)
        self.accelerate_hostile(dt)


        # Next, move the objects around the screen
        self.player.move(windowsize=Window.size)
        self.hostile.move(windowsize=Window.size)
        for asteroid in self.asteroids:
            asteroid.move(windowsize=Window.size)
        for shell in self.player.shells:
            shell.move(windowsize=Window.size)
            if shell.offscreen:
                self.player.shells.remove(shell)
                self.remove_widget(shell)
        for shell in self.hostile.shells:
            shell.move(windowsize=Window.size)
            if shell.offscreen:
                self.hostile.shells.remove(shell)
                self.remove_widget(shell)

        # Finally, check for any collisions
        self.detect_collisions()

    def check_collide_asteroid(self, asteroid):
        pass
        # for ship in self.spaceships:
        #     if asteroid.pos == ship.pos:
        #         self.asteroids.remove(asteroid)
        #         self.ids.GameView.remove_widget(asteroid)
        # for other_asteroid in self.asteroids:
        #     if other_asteroid == asteroid:
        #         pass
        #     elif other_asteroid.pos == asteroid.pos:
        #         self.asteroids.remove(asteroid)
        #         self.asteroids.remove(other_asteroid)
        #         self.ids.GameView.remove_widget(asteroid)
        #         self.ids.GameView.remove_widget(other_asteroid)

    def new_remove_widget(self, widget_object):
        self.ids.GameView.remove_widget(widget_object)


    def detect_collisions(self):
        print("xxxxxxxx", self.collidables)
        for object in self.collidables:
            for other_object in self.collidables:
                if object != other_object:
                    if object.collide_widget(other_object):
                        if object == self.player or other_object == self.player:
                            pass
                        self.new_remove_widget(object)
                        self.collidables.remove(object)
                        self.new_remove_widget(other_object)
                        self.collidables.remove(other_object)


        #     if self.hostile.collide_widget(asteroid):
        #         self.remove_asteroid(asteroid)
        #         Logger.info("Collision: Hostile to Asteroid")
        #     if self.player.collide_widget(asteroid):
        #         self.remove_asteroid(asteroid)
        #         Logger.info("Collision: Hostile to Player")

        # for ship in self.spaceships:
        #     for object in self.asteroids:
        #         if ship.collide_widget(object):
        #             sound = SoundLoader.load('explosion1.ogg')
        #             sound.play()
        #             Logger.info("Ship 2 Object Collision Detected!")
        #             self.new_remove_widget(self.ship)
        #     for shell in self.shells:
        #         if ship.collide_widget(shell):
        #             sound = SoundLoader.load('explosion1.ogg')
        #             sound.play()
        #             Logger.info("Ship 2 Laser Collision Detected!")
        #             self.new_remove_widget(self.ship)

        # for shell in self.player.shells:
        #     if self.hostile.collide_widget(shell):
        #         sound = SoundLoader.load('explosion1.ogg')
        #         sound.play()
        #          Logger.info("Ship 2 Shot Collision Detected!")
        #          Logger.info(str(len(self.spaceships)))
        #          self.new_remove_widget(self.hostile)
        #     for asteroid in self.asteroids:
        #         if self.hostile.collide_widget(asteroid):
        #          Logger.info("astroid 2 Shot Collision Detected!")
        #          Logger.info(str(len(self.spaceships)))
        #     sound = SoundLoader.load('explosion1.ogg')
        #     sound.play()
        #
        # for asteroid in self.asteroids:
        #     if self.player.collide_widget(asteroid):
        #      Logger.info("Ship 2 Astroid Collision Detected!")
        #      self.new_remove_widget(self.asteroid)

    def generate_asteroid(self):
        # use left, bottom positions because asteroids can fly around screen
        positions = {
            'left':   Vector(0, randint(0, Window.size[1])),
            'bottom': Vector(randint(0, Window.size[0]), 0),
        }
        position = choice(list(positions.values()))
        asteroid = AsteroidObj()
        asteroid.pos = position
        asteroid.angle = randint(0, 360)
        asteroid.speed = 1
        self.ids.GameView.add_widget(asteroid)
        # self.add_widget(asteroid)
        self.asteroids.append(asteroid)
        return asteroid


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
