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
            'text': 'Esc',
            'command': 'k{esc}',
            'column': 2,
            'row': 6
        },
        {
            'text': 'Up',
            'command': 'k{up}',
            'column': 3,
            'row': 6
        },
        {
            'text': 'Subtitles',
            'command': 'kx',
            'column': 4,
            'row': 6
        },
        {
            'text': 'Left',
            'command': 'k{left}',
            'column': 2,
            'row': 7
        },
        {
            'text': 'Enter',
            'command': 'k{enter}',
            'column': 3,
            'row': 7
        },
        {
            'text': 'Right',
            'command': 'k{right}',
            'column': 4,
            'row': 7
        },
        {
            'text': 'Guide',
            'command': 'k{f1}',
            'column': 2,
            'row': 8
        },
        {
            'text': 'Down',
            'command': 'k{down}',
            'column': 3,
            'row': 8
        },
        {
            'text': 'Play/Pause',
            'command': 'k{playpause}',
            'column': 4,
            'row': 8
        },
    ]
}