"""The Spaced Out app configuration."""
from os import path
from kivy.resources import resource_add_path

paths = {
    'images': path.join('assets', 'images')
    }

resource_add_path(paths['images'])
