"""Ship entities that start from Kivy widgets and branch into player/enemies.

Ships have the following stats:

    Attack - The ships effectiveness at doing damage.
    Speed - The ships ability to accelerate and its top speed.
    HP - The maximum out of damage the ship can sustain.
    Ammo - The ships capacity to carry ammunition.

"""
from kivy.logger import Logger
from kivy.uix.widget import Widget

from spacegame.data.ships import hostiles, players
from kivy.properties import (
    ObjectProperty, NumericProperty, BooleanProperty, StringProperty,
    ListProperty,
)

class BaseShip(Widget):
    """The base ship sets each stat to 1."""
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity = NumericProperty(0)

    skin = StringProperty(0)
    stats = None
    type = StringProperty(0)

    def __init__(self, shiptype='basic', dataset=None, **kwargs):
        super().__init__(**kwargs)
        self.load(shiptype, dataset)

    def load(self, type, dataset):
        """Load the stats according to type.

        Args:
            type (str): The key in data/ships.py to load the stats from.
            dataset (obj): The object to pull stats from.
        """
        Logger.info('Loading {} ship type.'.format(type))
        data = getattr(dataset, type)
        if data is None:
            raise KeyError('"{}" is not a ship type in `config`.'.format(type))

        self.type = type
        self.skin = data['skin']
        self.stats = data['stats']

        Logger.info('Skin {}.'.format(data['skin']))
        Logger.info('Stats {}.'.format(data['stats']))

    def stat(self, key):
        """Retrieve a stat value from stats.

        Args:
            key (str): The name of the stat to get.

        """
        value = self.stats.get(key)
        if value is None:
            raise KeyError('"{}" is not a stat.'.format(key))

        return value


class HostileShip(BaseShip):
    difficulty = None
    modifier = 1

    def __init__(self, shiptype='basic', dataset=hostiles, **kwargs):
        super().__init__(shiptype=shiptype, dataset=dataset, **kwargs)

    def load(self, type, difficulty=None):
        """Load the stats according to type.

        Args:
            type (str): The key in data/ships.py to load the stats from.

        """
        super().load(type, hostiles)
        if difficulty is not None:
            modifier = getattr(hostiles, difficulty)
            if modifier is None:
                raise KeyError(
                    '"{}" is not a difficulty in `hostiles`.'.format(difficulty)
                    )

            self.difficulty = difficulty
            self.modifier = modifier

    def stat(self, key, modified=True):
        """Load the stat with the option to include the modifier or not.

        Args:
            key (str): The name of the stat to lookup.
            modified (bool): Apply the modifier or not. Defaults to True.

        """
        modifier = self.modifier if modified else 1
        return modifier * super().stat(key)


class PlayerShip(BaseShip):

    def __init__(self, shiptype='basic', dataset=players, **kwargs):
        super().__init__(shiptype=shiptype, dataset=dataset, **kwargs)
