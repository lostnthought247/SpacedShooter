"""Ship entities that start from Kivy widgets and branch into player/enemies.

Ships have the following stats:

    Attack - The ships effectiveness at doing damage.
    Speed - The ships ability to accelerate and its top speed.
    HP - The maximum out of damage the ship can sustain.
    Ammo - The ships capacity to carry ammunition.

"""
from kivy.logger import Logger
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget

from spacegame.data.ships import hostiles, players
from spacegame.entities.weapons import PlayerWeapons


class BaseShip(Widget):
    """The base ship loads common properties from a dataset in data/ships.

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
    lastfired = 0.0
    shells = ListProperty()
    skin = StringProperty()
    speed = NumericProperty(0)
    stats = None
    type = StringProperty()
    weaponstype = StringProperty()

    def __init__(self, shiptype='basic', dataset=None, **kwargs):
        super().__init__(**kwargs)
        self.dataset = dataset
        self.load(shiptype)

    def load(self, type):
        """Load the ship data according to type.

        Args:
            type (str): The key in data/ships.py to load the data from.

        """
        Logger.debug('Entities: Loading "{}" ship type.'.format(type))
        data = getattr(self.dataset, type)
        if data is None:
            raise KeyError(
                '"{}" is not a ship type in `dataset`.'.format(type)
                )

        self.type = type
        self.skin = data['skin']
        self.stats = data['stats']
        self.weaponstype = data['weapons']

        Logger.debug('Entities: Ship Skin: {}.'.format(data['skin']))
        Logger.debug('Entities: Ship Stats: {}.'.format(data['stats']))

    def move(self, windowsize=(None, None)):
        """Advance the player ship position according to its velocity."""
        delta = Vector(self.speed, 0).rotate(self.angle)
        self.pos = delta + self.pos
        for i in [0, 1]:  # Wrap the screen.
            if self.pos[i] < -5:
                self.pos[i] = windowsize[i]
            elif self.pos[i] > windowsize[i]+10:
                self.pos[i] = 0

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
        """Load the data from a hostiles dataset according to type.

        Args:
            type (str): The key in data/ships.py to load the stats from.
            difficulty (str): The key to load the difficulty from.

        """
        super().load(type)
        if difficulty is not None:
            modifier = getattr(self.dataset, difficulty)
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

    def fire(self):
        """Fire the ship's weapons."""
        Logger.debug('Entities: Firing weapons.')
        shell = PlayerWeapons(weapontype=self.weaponstype)

        Logger.debug('Entities: Last Fired: {}'.format(self.lastfired))
        if self.lastfired >= shell.stats['recharge']:
            self.lastfired = 0.0

            # Position the shell in front of the ship.
            shell.angle = self.angle
            shell.speed = shell.stats['speed']
            shell.pos = (0, 0)

            # Add the shell to the list of fired weapons to track.
            self.shells.append(shell)
            self.add_widget(shell)

            Logger.debug('Entities: Bombs away!')
        else:
            Logger.debug('Entities: Weapons are not charged.')
