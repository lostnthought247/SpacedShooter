"""Ship weapons."""
from kivy.logger import Logger
from kivy.vector import Vector

from spacegame.data.weapons import hostiles, players
from spacegame.entities.widget import Widget


class BaseWeapons(Widget):
    """The base weapons loads common properties from data/weapons.

    Attributes:
        offscreen (bool): True if the shell is not visible. False otherwise.

    """

    def __init__(self, type='lasers', dataset=None, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)
        self.offscreen = False

    def load(self, type):
        """Change the weapon to another type in the dataset.

        Args:
            type (str): The key in data/weapons.py to load the data from.

        """
        super().load(type)
        self.sfx = self.datum('sfx')
        self.stats = dict(self.datum('stats'))
        Logger.debug('Entities: Weapon SFX: {}.'.format(self.sfx))

    def move(self, windowsize=(None, None)):
        """Advance the weapon's fire according to its velocity."""
        delta = Vector(self.speed, 0).rotate(self.angle)
        self.pos = delta + self.pos
        for i in [0, 1]:  # Mark offscreen projectiles for deletion.
            if self.pos[i] < -5 or self.pos[i] > windowsize[i]:
                self.offscreen = True
                self.pos = (-10000, -10000)
                break


class HostileWeapons(BaseWeapons):
    """Hostile weapons default to a specific dataset."""

    def __init__(self, type='lasers', dataset=hostiles, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)


class PlayerWeapons(BaseWeapons):
    """Player weapons default to a specific dataset."""

    def __init__(self, type='lasers', dataset=players, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)
