# -*- coding: utf-8 -*-

import os
import sys

from glue.bin import main

if __name__ == '__main__':
    main([
        'glue',
        '-f',
        '--source=./emojis/',
        '--img=../trac_emoji/htdocs/',
        '--css=../trac_emoji/htdocs/css',
        '--namespace=emoji',
        '--sprite-namespace=',
        '--margin=10',
        '--css-template=./emoji_template.jinja'
    ])

    candidates = []
    for name in os.listdir('./emojis/'):
        if name.endswith('.png'):
            candidates.append(name[:-4])
    candidates.sort()

    f = open('../trac_emoji/emojis.py', 'w')
    f.write("""
# -*- coding: utf-8 -*-

candidates = [
""")
    for candidate in candidates:
        f.write('\'{}\',\n'.format(candidate))
    f.write("""
]
""")
    f.close()
