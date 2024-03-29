"""The ship data that describes each type of player ship."""

fast = {
    'skin': 'ship1.png',
    'states': {
        'exploded': {
            'skin': 'boom.png',
            'sfx': 'explosion.ogg',
            },
        },
    'stats': {
        'attack': 1,
        'speed': 9,
        'hp': 3,
        'ammo': 50,
        },
    'weapons': 'lasers',
    }

basic = {
    'skin': 'ship2.png',
    'states': {
        'exploded': {
            'skin': 'boom.png',
            'sfx': 'explosion.ogg',
            },
        },
    'stats': {
        'attack': 6,
        'speed': 5,
        'hp': 5,
        'ammo': 75,
        },
    'weapons': 'lasers',
    }

tank = {
    'skin': 'ship3.png',
    'states': {
        'exploded': {
            'skin': 'boom.png',
            'sfx': 'explosion.ogg',
            },
        },
    'stats': {
        'attack': 5,
        'speed': 3,
        'hp': 8,
        'ammo': 100,
        },
    'weapons': 'lasers',
    }
