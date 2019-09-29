"""Ship entities that start from Kivy widgets and branch into player/enemies.

Ships have the following stats:

    Attack - The ships effectiveness at doing damage.
    Speed - The ships ability to accelerate and its top speed.
    HP - The maximum out of damage the ship can sustain.
    Ammo - The ships capacity to carry ammunition.

"""
from kivy.logger import Logger
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.widget import Widget

from spacegame.data.ships import hostiles, players


class BaseShip(Widget):
    """The base ship loads common properties from a dataset in data/ships.

    Args:
        shiptype (str): The type of ship to instantiate.
        dataset (obj): The module containing the ship data.

    Attributes:
        angle (int): The rotation angle of the ship in degrees.
        skin (str): The ship's image without the path (images go in
            assets/images).
        speed (float): The current speed of the ship in made up units.
        stats (dict): The ships stats. Stats come from spacegame.data.ships.
        type (str): The key that ship data was loaded from.

    """

    angle = NumericProperty(0)
    skin = StringProperty(0)
    speed = NumericProperty(0)
    stats = None
    type = StringProperty(0)

    def __init__(self, shiptype='basic', dataset=None, **kwargs):
        super().__init__(**kwargs)
        self.dataset = dataset
        self.load(shiptype)

    def load(self, type):
        """Load the stats according to type.

        Args:
            type (str): The key in data/ships.py to load the stats from.

        """
        Logger.debug('Entities: Loading {} ship type.'.format(type))
        data = getattr(self.dataset, type)
        if data is None:
            raise KeyError('"{}" is not a ship type in `config`.'.format(type))

        self.type = type
        self.skin = data['skin']
        self.stats = data['stats']

        Logger.debug('Entities: Skin: {}.'.format(data['skin']))
        Logger.debug('Entities: Stats: {}.'.format(data['stats']))

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
    """Hostile ships default to a specific dataset and have modifiers.

    Attributes:
        difficulty (str): The key used to look up the difficulty modifier in
            the dataset.
        modifier (float): A factor to apply to stats.

    """

    difficulty = None
    modifier = 1

    def __init__(self, shiptype='basic', dataset=hostiles, **kwargs):
        super().__init__(shiptype=shiptype, dataset=dataset, **kwargs)

    def load(self, type, difficulty=None):
        """Load the stats according to type.

        Args:
            type (str): The key in data/ships.py to load the stats from.
            difficulty (str): The key to load the difficulty from.

        """
        super().load(type, hostiles)
        if difficulty is not None:
            modifier = getattr(hostiles, difficulty)
            if modifier is None:
                raise KeyError(
                    '"{}" is not a key in `hostiles`.'.format(difficulty)
                    )

            self.difficulty = difficulty
            self.modifier = modifier
            Logger.debug('Entities: Difficulty: {}.'.format(difficulty))
            Logger.debug('Entities: Modifier: {}.'.format(modifier))

    def stat(self, key, modified=True):
        """Load the stat with the option to apply the modifier or not.

        Args:
            key (str): The name of the stat to lookup.
            modified (bool): Apply the modifier or not. Defaults to True.

        """
        modifier = self.modifier if modified else 1
        return modifier * super().stat(key)


class PlayerShip(BaseShip):
    """Player ships default to a specific dataset and have access to boosts."""

    def __init__(self, shiptype='basic', dataset=players, **kwargs):
        super().__init__(shiptype=shiptype, dataset=dataset, **kwargs)
