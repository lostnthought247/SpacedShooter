"""Object entities that start from Kivy widgets.

objects have the following stats:

    skin - The image for the object
    type - The type of object


"""
from kivy.logger import Logger
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget

from spacegame.data.ships import hostiles, players
from spacegame.data.objects import collectables, explodables, obstacles
from spacegame.entities.weapons import PlayerWeapons
from random import randint

class BaseObject(Widget):
    """The base object loads common properties from a dataset in data/ships.

    Args:
        shiptype (str): The type of ship to instantiate.
        dataset (obj): The module containing the ship data.

    Attributes:
        angle (int): The rotation angle of the ship in degrees.
        dataset (obj): The data module the ship belongs to.
        lastfired (float): The time since weapons were fired last.
        skin (str): The ship's image without the path (images go in
            assets/images).
        speed (float): The current speed of the ship in made up units.
        stats (dict): The ships stats. Stats come from spacegame.data.ships.
        type (str): The key that ship data was loaded from.
        weaponstype (str): The key that weapons data was loaded from.

    """

    angle = NumericProperty(0)
    skin = StringProperty()
    speed = NumericProperty(0)
    type = StringProperty()

    def __init__(self, objtype='basic', dataset=None, **kwargs):
        super().__init__(**kwargs)
        self.dataset = dataset
        self.load(objtype)

    def load(self, type):
        """Load the object data according to type.

        Args:
            type (str): The key in data/objects.py to load the data from.

        """
        Logger.debug('Entities: Loading "{}" ship type.'.format(type))
        data = getattr(self.dataset, type)
        if data is None:
            raise KeyError(
                '"{}" is not a object type in `dataset`.'.format(type)
                )

        self.type = type
        self.skin = data['skin']

        Logger.debug('Entities: Object Skin: {}.'.format(data['skin']))


    def move(self, windowsize=(None, None)):
        """Advance the player ship position according to its velocity."""
        delta = Vector(self.speed, 0).rotate(self.angle)
        self.pos = delta + self.pos
        for i in [0, 1]:  # Wrap the screen.
            if self.pos[i] < -5:
                self.pos[i] = windowsize[i]
            elif self.pos[i] > windowsize[i]+10:
                self.pos[i] = 0
