from os import environ

SESSION_CONFIGS = [
    dict(
        name='show_payoff',
        display_name='利得提示群',
        num_demo_participants=20,
        app_sequence=['imitation'],
        condition='提示群',
    ),
    dict(
        name='hide_payoff',
        display_name='利得非提示群',
        num_demo_participants=20,
        app_sequence=['imitation'],
        condition='非提示群',
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

LANGUAGE_CODE = 'ja'
POINTS_CUSTOM_NAME = 'ポイント'

ROOMS = []

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'secret'

INSTALLED_APPS = ['otree']
