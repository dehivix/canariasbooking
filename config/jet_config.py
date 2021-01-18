from django.utils.translation import ugettext_lazy as _

# JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
# JET_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'

# JET_MODULE_YANDEX_METRIKA_CLIENT_ID = '46de85bff0f94c82bbf42be177f128a2'
# JET_MODULE_YANDEX_METRIKA_CLIENT_SECRET = '01107ac1049b49ab9b24e60e95ba2a93'

JET_SIDE_MENU_ITEMS = [
    # {'label': _('Load CSV'), 'items': [
    #     {'label': _('Load New Tasks'), 'url': '/admin/loadBatchTask/', 'url_blank': False},
    #     {'label': _('Load Translations of Tasks'), 'url': '/admin/loadBatchTranslations/', 'url_blank': False},
    #     {'label': _('Load Tips'), 'url': '/admin/loadBatchTips/', 'url_blank': False},
    # ]},

    # {'label': _('Translate Dashboard'), 'items': [
    #     {'label': _('Make/Edit Translations'), 'url': '/rosetta/', 'url_blank': True},
    # ]},

    {'app_label': 'hotels', 'items': [
        {'name': 'habitaciones'},
        {'name': 'tipohabitacion'},
    ]},

    {'app_label': 'bookings', 'items': [
        {'name': 'reservas'},
    ]},
]

# jet theme
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
