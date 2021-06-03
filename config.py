COLUMNS = 4
ROWS = 8

PROGRAMS = {
    'NextPVR': '"C:\\Program Files\\NextPVR\\client\\NextPVR.exe"'
}

PAGES = {
    'Main': [
        {
            'text': 'NextPVR',
            'href': '/page/NextPVR'
        },
        {
            'text': 'A',
            'command': 'ka'
        },
        {
            'text': 'Enter',
            'command': 'k{enter}'
        },
        {
            'text': 'A',
            'command': 'ka'
        },
        {
            'text': 'Enter',
            'command': 'k{enter}'
        },
        {
            'text': 'A',
            'command': 'ka'
        },
        {
            'text': 'Enter',
            'command': 'k{enter}'
        }
    ],
    'NextPVR': [
        {
            'text': 'Back',
            'href': '/page/Main'
        },
        {
            'text': 'Launch NextPVR',
            'command': 'lNextPVR'
        },
        {
            'text': 'Recordings',
            'command': 'k{f8}'
        },
        {
            'text': ''
        },
        
        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },

        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },

        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },

        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },
        {
            'text': ''
        },

        {
            'text': ''
        },
        {
            'text': 'Esc',
            'command': 'k{esc}'
        },
        {
            'text': 'Up',
            'command': 'k{up}'
        },
        {
            'text': 'Subtitles',
            'command': 'kx'
        },

        {
            'text': ''
        },
        {
            'text': 'Left',
            'command': 'k{left}'
        },
        {
            'text': 'Enter',
            'command': 'k{enter}'
        },
        {
            'text': 'Right',
            'command': 'k{right}'
        },

        {
            'text': ''
        },
        {
            'text': 'Guide',
            'command': 'k{f1}'
        },
        {
            'text': 'Down',
            'command': 'k{down}'
        },
        {
            'text': 'Play/Pause',
            'command': 'k{playpause}'
        },
    ]
}