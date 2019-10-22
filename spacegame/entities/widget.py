"""Widgets are spacegame entities that start from Kivy widgets."""

from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.vector import Vector
import kivy.uix.widget


class Widget(kivy.uix.widget.Widget):
    """The base object loads common properties from a dataset in data/objects.

    Game entities are loaded from data modules. The widget's dataset cannot
    change, but the type can.

    Args:
        type (str): The type of ship to instantiate.
        dataset (obj): The module containing the ship data.

    Attributes:
        angle (int): The rotation angle of the ship in degrees.
        skin (str): The ship's image without the path (images go in
            assets/images).
        speed (float): The current speed of the ship in made up units.

    """

    angle = NumericProperty(0)
    skin = StringProperty()
    speed = NumericProperty(0)

    def __init__(self, type='entity', dataset=None, **kwargs):
        """Set the widget's dataset and load it's default type."""
        super().__init__(**kwargs)
        self.dataset = dataset
        self.load(type)

    def datum(self, key, default=None):
        """Retrieve an attribute from the dataset according to type."""
        return getattr(self.dataset, self.type).get(key, default)

    def load(self, type):
        """Change the widget's type to another type in the dataset.

        If the type is the same as before, the attributes are copied from the
        dataset again.

        Args:
            type (str): The key in the data file to load from.

        """
        Logger.debug('Entities: Loading "{}" entity type.'.format(type))

        self.type = type
        self.skin = self.datum('skin')
        self.speed = self.datum('speed', default=0)
        self.angle = self.datum('angle', default=0)

        Logger.debug('Entities: Object Skin: {}.'.format(self.skin))

    def move(self, windowsize=(None, None)):
        """Advance the entity position according to its velocity."""
        delta = Vector(self.speed, 0).rotate(self.angle)
        self.pos = delta + self.pos
        for i in [0, 1]:  # Wrap the screen.
            if self.pos[i] < -5:
                self.pos[i] = windowsize[i]
            elif self.pos[i] > windowsize[i]:
                self.pos[i] = 0
