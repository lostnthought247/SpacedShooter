"""Manage various aspects of the game."""
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from math import sqrt
from os.path import basename


class Resource:
    """A resource and its subscribers.

    Resources without subscribers are unloaded from memory.

    Attributes:
        track (kivy.core.audio.Sound): A sound resource.
        subscribers (dict): A collection of objects using the resource.

    """

    def __init__(self, track):
        self.track = track
        self.subscribers = {}


class SoundManager:
    """Provide access to sound resources and play them at the right volume.

    Attributes:
        sfx (dict of Resources): Sound effects resources.
        music (dict): Music tracks.
        volumes (dict): The various volume levels: sfx, music, and master.

    """
    sfx = {}
    music = {}
    volumes = {
        'sfx': 1.0,
        'music': 1.0,
        'master': 1.0,
        }

    @classmethod
    def add_sfx(cls, source, subscriber):
        """Add an sfx track that will last in memory if there are subscribers.

        Args:
            source (str): The name of the sound to add.
            subscriber (obj): The object using the track.

        """
        fn = basename(source)
        try:  # Subscribe the subscriber to the sfx resource.
            resource = cls.sfx[fn]
        except KeyError:  # Create the sfx resource and subscribe.
            track = SoundLoader.load(fn)
            track.volume = cls.sfx_volume()
            resource = Resource(track)
            cls.sfx[fn] = resource
        resource.subscribers[subscriber] = subscriber

    @classmethod
    def remove_sfx(cls, source, subscriber):
        """Remove one of the sfx track or its subscriber.

        Args:
            source (str): The filename of the track to remove.
            subscriber (obj): The object no longer using the track.

        """
        fn = basename(source)
        resource = cls.sfx[fn]
        del resource.subscribers[subscriber]
        if len(resource.subscribers) == 0:
            del cls.sfx[fn]
            resource.track.unload()

    @classmethod
    def play_sfx(cls, source):
        """Play one of the sfx tracks.

        Args:
            source (str): The filename or path to play.

        """
        resource = cls.sfx[basename(source)]
        resource.track.play()

    @classmethod
    def update_sfx(cls):
        """Apply the current music volume levels to all the music tracks."""
        for resource in cls.sfx:
            resource.track.volume = cls.sfx_volume()

    @classmethod
    def sfx_volume(cls, volume=None):
        """Get or set the sfx volume.

        The sfx volume modifies the volume of sfx sounds.

        Args:
            volume (int): The sfx volume to set from 0 to 1.

        """
        if volume is not None:
            cls.volumes['sfx'] = volume
            cls.update_sfx()

        return cls.scale(cls.volumes['sfx'], cls.master_volume())

    @classmethod
    def add_music(cls, source, subscriber):
        """Add a music track.

        Args:
            source (str): The name of the music to add.
            subscriber (obj): The object using the track.

        """
        fn = basename(source)
        try:  # Subscribe the subscriber to the music resource.
            resource = cls.music[fn]
        except KeyError:  # Create the music resource and subscribe.
            track = SoundLoader.load(fn)
            track.volume = cls.music_volume()
            resource = Resource(track)
            cls.music[fn] = resource
        resource.subscribers[subscriber] = subscriber

    def remove_music(cls, source, subscriber):
        """Remove one of the music tracks or its subscriber.

        Args:
            source (str): The filename of the track to remove.
            subscriber (obj): The object no longer using the track.

        """
        fn = basename(source)
        resource = cls.music[fn]
        del resource.subscribers[subscriber]
        if len(resource.subscribers) == 0:
            del cls.music[fn]
            resource.track.unload()

    @classmethod
    def play_music(cls, source):
        """Play one of the music tracks.

        Args:
            source (str): The filename or path to play.

        """
        track = cls.music[basename(source)]
        track.play()

    @classmethod
    def update_music(cls):
        """Apply the current music volume levels to all the music tracks."""
        for track in cls.music:
            track.volume = cls.music_volume()

    @classmethod
    def music_volume(cls, volume=None):
        """Get or set the music volume.

        The music volume modifies the volume of music sounds.

        Args:
            volume (int): The music volume to set from 0 to 1.

        """
        if volume is not None:
            cls.volumes['music'] = volume
            cls.update_music()

        return cls.scale(cls.volumes['music'], cls.master_volume())

    @classmethod
    def master_volume(cls, volume=None):
        """Get or set the master volume.

        The master volume modifies the volume of all audio.

        Args:
            volume (int): The master volume to set from 0 to 1.

        """
        if volume is not None:
            cls.volumes['master'] = volume
            cls.update_sfx()
            cls.update_music()

        return cls.volumes['master']

    @staticmethod
    def scale(*volumes):
        """Return the volume after combining multiple volume settings.

        The volume is scaled to roll off smoothly and slowly. It preserves
        a lot of the volume, but is still zero if any of the volumes are zero.

        f(x_1, x_2, ..., x_n)=sqrt(n*x_1*x_2*...x_n)/sqrt(n)

        Args:
            volumes (list): The volumes to combine into a scaled volume.

        Returns:
            float: A value between 0 and 1.

        """
        product = 1
        for volume in volumes:
            product *= volume

        scaled = sqrt(len(volumes)*product) / sqrt(len(volumes))
        Logger.debug("The volume set of {} is {}.".format(volumes, scaled))
        return scaled
