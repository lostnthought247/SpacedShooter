"""The ship data that describes each type of hostile ship."""

fast = {
    'skin': 'hostile1.png',
    'stats': {
        'attack': 1,
        'speed': 9,
        'hp': 3,
        'ammo': 50,
        },
    'weapons': 'lasers',
    }

basic = {
    'skin': 'hostile2.png',
    'stats': {
        'attack': 5,
        'speed': 5,
        'hp': 5,
        'ammo': 75,
        },
    'weapons': 'lasers',
    }

tank = {
    'skin': 'hostile3.png',
    'stats': {
        'attack': 7,
        'speed': 1,
        'hp': 8,
        'ammo': 100,
        },
    'weapons': 'lasers',
    }

easy = 0.5
medium = 1
hard = 2
