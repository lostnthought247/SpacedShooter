from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.lang import Builder
from kivy.uix.label import CoreLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


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


class PlayerShip(Widget):
    """The player's ship."""
    Speed = None
    HP = None
    Attack = None

    def move_player(self):
        """Move the player's ship 10 units on each axis."""
        newX = self.pos[0] + 10
        newY = self.pos[1] + 10
        self.pos = (newX, newY)


class IntroScreen(Screen):
    """The very first screen with options to start, continue, or quit."""
    pass


class BaseScreen(Screen):
    """The home base screen where a user selects the ship to use."""
    selected_ship = "ship1.png"
    ship_speed = 100
    ship_hp = 100
    ship_attack = 100


class CombatScreen(Screen):
    """The screen that the user flies around shooting enemies."""
    player = PlayerShip()
    player.move_player()


class ReturnScreen(Screen):
    """The screen for choosing a saved game to continue."""
    pass


class ScreenManagement(ScreenManager):
    """A class to reference in the .kv file for managing screens."""
    pass


class SpaceGame(Widget):
    """The game itself."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.score_label = CoreLabel(text="Score: 0")
        self.score_label.refresh()

        with self.canvas:
            self.player = Rectangle(
                source="Hero.png",
                pos=(0, 0),
                size=(Window.width / 4, Window.height / 4)
                )
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
            self.score_instruction = Rectangle(
                texture=self.score_label.texture,
                pos=(0, Window.height - 50),
                size=self.score_label.texture.size
                )

        # Create a set of pressed keys for the given moment
        self.keysPressed = set()

        # Set the event interval of every frame
        Clock.schedule_interval(self.move_hero, 0)

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


class SpaceGameApp(App):
    """The kivy application."""

    def build(self):
        """Build the app and return an app object that can be run."""
        # Loads and builds view based on SpaceGame.kv file
        presentation = Builder.load_file("SpaceGame.kv")

        return presentation


if __name__ == "__main__":
    """Run the application when the script is executed."""
    SpaceGameApp().run()
