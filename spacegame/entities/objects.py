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
        ...
    Attributes:
        ...

    """

    angle = NumericProperty(0)
    skin = StringProperty()
    speed = NumericProperty(0)
    type = StringProperty()

    def __init__(self, objtype='lg_asteroid', dataset=None, **kwargs):
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
            elif self.pos[i] > windowsize[i]:
                self.pos[i] = 0

    def temp_get_asteroid(self):
            asteroid_img = "rock_stone_lg.png"
            return asteroid_img



class AsteroidObj(BaseObject):
    def __init__(self, objtype='lg_asteroid', dataset=obstacles, **kwargs):
        super().__init__(objtype=objtype, dataset=dataset, **kwargs)

        self.angle = randint(-360,360)
        self.speed = randint(1,5)/2.5
