"""Ship entities that start from game widgets and branch into player/enemies.

Ships have the following stats:

    Attack - The ships effectiveness at doing damage.
    Speed - The ships ability to accelerate and its top speed.
    HP - The maximum out of damage the ship can sustain.
    Ammo - The ships capacity to carry ammunition.

"""
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty

from spacegame.data.ships import hostiles, players
from spacegame.entities.weapons import HostileWeapons, PlayerWeapons
from spacegame.entities.widget import Widget
from spacegame.managers import SoundManager


class BaseShip(Widget):
    """The base ship loads common properties from a dataset in data/ships.

    Attributes:
        lastfired (float): The time since weapons were fired last.
        stats (dict): The ships stats. Stats come from spacegame.data.ships.
        weapontype (str): The key that weapons data was loaded from.

    """

    shells = ListProperty()
    weapontype = StringProperty()

    def __init__(self, type='basic', dataset=None, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)
        self.weaponsound = None
        self.destroyed = False

    def load(self, type):
        """Change the ship's type to another type in the dataset.

        Args:
            type (str): The key in data/ships.py to load the stats from.
            difficulty (str): The key to load the difficulty from.

        """
        super().load(type)
        self.stats = dict(self.datum('stats'))
        self.weapontype = self.datum('weapons')
        self.lastfired = 0.0
        Logger.debug('Entities: Ship Stats: {}.'.format(self.stats))
        Logger.debug('Entities: Ship Weapontype: {}.'.format(self.weapontype))

    def stat(self, key):
        """Retrieve a stat value from stats.

        Args:
            key (str): The name of the stat to get.

        """
        return self.stats.get(key)


class HostileShip(BaseShip):
    """Hostile ships default to a specific dataset and have modifiers.

    Attributes:
        difficulty (str): The key used to look up the difficulty modifier in
            the dataset.
        modifier (float): A factor to apply to stats.

    """

    def __init__(self, type='basic', dataset=hostiles, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)
        self.obj_type = "hostile_ship"


    def load(self, type, difficulty=None):
        """Change the ship's type to another type in the dataset.

        Args:
            type (str): The key in data/ships.py to load the stats from.
            difficulty (str): The key to load the difficulty from.

        """
        super().load(type)
        self.difficulty = None
        self.modifier = 1
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

    def fire(self):
        """Fire the ship's weapons."""
        Logger.debug('Entities: Firing weapons.')
        shell = HostileWeapons(type=self.weapontype)

        if shell.sfx != self.weaponsound:  # The sound effect has changed.
            # Remove the old sound effect.
            if self.weaponsound is not None:
                sfx = SoundManager.sfx.get(self.weaponsound)
                SoundManager.remove_sfx(sfx, self)

            # Add the new sound effect.
            self.weaponsound = shell.sfx
            SoundManager.add_sfx(shell.sfx, self)

        Logger.debug('Entities: Last Fired: {}'.format(self.lastfired))
        if self.lastfired >= shell.stats['recharge']:
            self.lastfired = 0.0

            # Position the shell in front of the ship.
            shell.origin = "hostile"
            shell.angle = self.angle
            shell.speed = shell.stats['speed']
            shell.pos = self.pos

            # Add the shell to the list of fired weapons to track.
            self.shells.append(shell)
            self.parent.add_widget(shell)
            SoundManager.play_sfx(shell.sfx)

            Logger.debug('Entities: Bombs away!')
        else:
            Logger.debug('Entities: Weapons are not charged.')


class PlayerShip(BaseShip):
    """Player ships default to a specific dataset and have access to boosts."""

    def __init__(self, type='basic', dataset=players, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)
        self.obj_type = "player_ship"
        self.lives = 3
        self.exp = 0
        self.level = 1

    def fire(self):
        """Fire the ship's weapons."""
        Logger.debug('Entities: Firing weapons.')
        shell = PlayerWeapons(type=self.weapontype)

        if shell.sfx != self.weaponsound:  # The sound effect has changed.
            # Remove the old sound effect.
            if self.weaponsound is not None:
                sfx = SoundManager.sfx.get(self.weaponsound)
                SoundManager.remove_sfx(sfx, self)

            # Add the new sound effect.
            self.weaponsound = shell.sfx
            SoundManager.add_sfx(shell.sfx, self)

        Logger.debug('Entities: Last Fired: {}'.format(self.lastfired))
        if self.lastfired >= shell.stats['recharge']:
            self.lastfired = 0.0

            # Position the shell in front of the ship.
            shell.origin = "player"
            shell.angle = self.angle
            shell.speed = shell.stats['speed']
            shell.pos = self.pos

            # Add the shell to the list of fired weapons to track.
            self.shells.append(shell)
            self.parent.add_widget(shell)
            SoundManager.play_sfx(shell.sfx)

            Logger.debug('Entities: Bombs away!')
        else:
            Logger.debug('Entities: Weapons are not charged.')
