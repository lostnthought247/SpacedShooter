"""Put all the pieces together to form the Spaced Out! application.

Run the application by importing the `SpaceGameApp` class and calling its
`run()` method. For example::

    from spacegame.app import SpaceGameApp
    SpaceGameApp().run()

"""
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger


class SpaceGameApp(App):
    """The kivy application."""

    def build(self):
        """Build the app and return an app object that can be run."""
        Logger.info('Application: Kivy has finally finished loading.')
        Logger.info('Application: Building "Spaced Out!" so you can run it...')
        presentation = Builder.load_file("app.kv")
        Logger.info('Application: ...Built. Run it by calling `self.run()`.')
        return presentation
