"""Obstacle entities that start from the spacegame widget."""
from random import randint

from spacegame.data.objects import obstacles
from spacegame.entities.widget import Widget


class BaseObstacle(Widget):
    """The base obstacle loads commonalities from data/objects."""

    def __init__(self, type='lg_asteroid', dataset=None, **kwargs):
        super().__init__(type=type, dataset=dataset, **kwargs)
        self.destroyed = False


class AsteroidObstacle(BaseObstacle):
    """Asteroid obstacles default to a specific dataset."""

    def __init__(self, type='lg_asteroid', dataset=obstacles, **kwargs):
        """Randomize the asteroid's speed and trajectory."""
        super().__init__(type=type, dataset=dataset, **kwargs)
        self.obj_type = "asteroid"

    def randomize_trajectory(self):
        """Choose a random angle and speed for the asteroid."""
        self.angle = randint(-360, 360)
        self.speed = randint(1, 5)/2.5
