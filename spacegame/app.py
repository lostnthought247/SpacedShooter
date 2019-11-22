"""Put all the pieces together to form the Spaced Out! application.

Run the application by importing the `SpaceGameApp` class and calling its
`run()` method. For example::

    from spacegame.app import SpaceGameApp
    SpaceGameApp().run()

"""
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import StringProperty


class SpaceGameApp(App):
    """The kivy application.

    Attributes:
        difficulty (str): The game's current level of difficulty.

    """
    difficulty = StringProperty('medium')


    def build(self):
        """Build the app and return an app object that can be run."""
        Logger.info('Application: Kivy has finally finished loading.')
        Logger.info('Application: Building "Spaced Out!" so you can run it...')
        presentation = Builder.load_file("app.kv")
        Logger.info('Application: ...Built. Run it by calling `self.run()`.')
        self.set_difficulty(difficulty='medium')
        return presentation

    def set_difficulty(self, difficulty='medium'):
        """Set the level of difficulty.

        Args:
            difficulty (str): The difficulty level to run the game at.

        """
        Logger.info(
            'Application: '
            'Setting the game difficulty to "{}".'.format(difficulty)
            )
