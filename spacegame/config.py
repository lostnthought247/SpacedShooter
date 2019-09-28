"""The Spaced Out app configuration."""
from os import path
from kivy.resources import resource_add_path

paths = {
    'images': path.join('assets', 'images'),
    'kv': path.join('spacegame', 'kv')
    }

resource_add_path(paths['images'])
resource_add_path(paths['kv'])
