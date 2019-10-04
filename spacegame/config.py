"""The Spaced Out app configuration."""
from os import path
from kivy.logger import Logger
from kivy.resources import resource_add_path

physics = {
    # A modifier that affects every ship's ability to accelerate.
    'acceleration': 0.25,

    # A modifier that affects every ship's ability to turn. Higher is faster.
    'turning': 25,
}


paths = {
    'images': path.join('assets', 'images'),
    'kv': path.join('spacegame', 'kv'),
    'sounds': path.join('assets', 'sounds')
    }

screens = {
    'Base': {
        'bg': [
            'dock.png',
            ],
    },
    'Combat': {
        'bg': [
            'space1.png',
            'space2.png',
            'space3.png',
            'space4.png',
            ],
    },
    'Intro': {
        'bg': [
            'space.png',
            ],
    },
    'Return': {
        'bg': [
            'space.png',
            ],
    },
    'Settings': {
        'bg': [
            'space.png',
            ],
        'selected_bg': (1, 1, 1, .75),
        'selected_color': (0, 0, 0, 1),
        'unselected_bg': (0, 0, 1, 0),
        'unselected_color': (1, 1, 1, 1),
    },
}

Logger.info('Config: Adding resource path "{}"'.format(paths['images']))
resource_add_path(paths['images'])

Logger.info('Config: Adding resource path "{}"'.format(paths['kv']))
resource_add_path(paths['kv'])

Logger.info('Config: Adding resource path "{}"'.format(paths['sounds']))
resource_add_path(paths['sounds'])
