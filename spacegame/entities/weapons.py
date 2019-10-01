"""Ship weapons."""
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.core.window import Window

from spacegame.data.weapons import hostiles, players


class BaseWeapons(Widget):
    """The base weapons loads common properties from data/weapons.

    Attributes:
        angle (int): The rotation angle of the ship in degrees.
        moot (bool): True if the shell is no longer relevant. False otherwise.
        dataset (obj): The data module the weapon belongs to.
        skin (str): The weapon's image without the path (images go in
            assets/images).
        speed (float): The current speed of the ship in made up units.

    """
    lifetime = NumericProperty(1)
    angle = NumericProperty(0)
    charged = False
    moot = False
    skin = StringProperty()
    speed = NumericProperty(0)
    stats = None
    type = StringProperty()

    def __init__(self, weapontype='lasers', dataset=None, **kwargs):
        super().__init__(**kwargs)
        self.dataset = dataset
        self.load(weapontype)

    def load(self, type):
        """Load the weapon data according to type.

        Args:
            type (str): The key in data/weapons.py to load the data from.

        """
        Logger.debug('Entities: Loading "{}" weapon type.'.format(type))
        data = getattr(self.dataset, type)
        if data is None:
            raise KeyError(
                '"{}" is not a weapon type in `dataset`.'.format(type)
                )

        self.type = type
        self.skin = data['skin']
        self.stats = data['stats']
        self.charged = True

        Logger.debug('Entities: Weapon Skin: {}.'.format(data['skin']))
        Logger.debug('Entities: Weapon Speed: {}.'.format(data['skin']))

    def move(self):
        """Update the position of the weaponsfire."""
        for i in [0, 1]:
            if self.pos[i] < 0:
                self.pos[i] = Window.size[i]
            elif self.pos[i] > Window.size[i]:
                self.pos[i] = 0

        delta = Vector(self.speed, 0).rotate(self.angle)
        self.pos = delta + self.pos


class HostileWeapons(BaseWeapons):
    """Hostile weapons default to a specific dataset."""

    def __init__(self, weapontype='lasers', dataset=hostiles, **kwargs):
        super().__init__(weapontype=weapontype, dataset=dataset, **kwargs)


class PlayerWeapons(BaseWeapons):
    """Player weapons default to a specific dataset."""

    def __init__(self, weapontype='lasers', dataset=players, **kwargs):
        super().__init__(weapontype=weapontype, dataset=dataset, **kwargs)
