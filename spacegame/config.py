"""The Spaced Out app configuration."""
from os import path
from kivy.resources import resource_add_path

physics = {
    # A modifier that affects every ship's ability to accelerate.
    'acceleration': 0.25,

    # A modifier that affects every ship's ability to turn. Higher is faster.
    'turning': 25,
}

paths = {
    'images': path.join('assets', 'images'),
    'kv': path.join('spacegame', 'kv')
    }

resource_add_path(paths['images'])
resource_add_path(paths['kv'])
