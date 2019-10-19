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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

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

        # Populate round/level objects and collidable lists
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

    def update(self, dt):
        """Step the scene forward."""
        # First, step time forward.
        self.player.lastfired += dt
        self.hostile.lastfired += dt
        self.accelerate_hero(dt)
        if self.hostile in self.collidables:
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


    def new_remove_widget(self, widget_object):
        # removes widget from the GameView FloatLayout
        self.ids.GameView.remove_widget(widget_object)


    def detect_collisions(self):
        # loops through all non-shell objects looking for collisions
        for object in self.collidables:
            for other_object in self.collidables:
                # ignore self to self matches
                if object != other_object:
                    if object.collide_widget(other_object):
                        # Checks if players died
                        if object == self.player or other_object == self.player:
                            self.my_popup()

                        # Removes colliding objects
                        self.new_remove_widget(object)
                        self.collidables.remove(object)
                        self.new_remove_widget(other_object)
                        self.collidables.remove(other_object)

            # Creates list of current active shots/shells
            all_shells = []
            for shell in self.player.shells:
                all_shells.append(shell)
            for shell in self.hostile.shells:
                all_shells.append(shell)
            # Loops through current active shells checking for collisions
            for shell in all_shells:
                if object.collide_widget(shell):
                    # ignores self friendly fire for player shells
                    if object == self.player and shell.origin == "player":
                        pass
                    # ignores self friendly fire for hostile shells
                    elif object == self.hostile and shell.origin == "hostile":
                        pass
                    # Triggers round end notification if player collides
                    elif object == self.player or other_object == self.player:
                        self.my_popup()

                    # Removes object that collides with shells
                    else:
                        self.new_remove_widget(object)
                        self.collidables.remove(object)
                        #self.new_remove_widget(shell)
                        #self.shells.remove(shell)


    def my_popup(self):
    """ The popup that appears upon player death """

        # creates/formats popup content
        content = BoxLayout(orientation='vertical')
        image = Image(source="deadscreen.png", size_hint=(1,1))
        btn1 = Button(text='Exit', size_hint=(1,.2))
        content.add_widget(image)
        content.add_widget(btn1)

        # creates popup from content
        popup = Popup(title='You Crashed',title_align="center", content=content, size_hint=(.6,.6))

        # binds button to pop-up window close
        btn1.bind(on_press=popup.dismiss)

        # Opens popup
        popup.open()

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
