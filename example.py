#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
from increasing import ProgressBar


p = ProgressBar([
    {
        'type': 'text'
    },
    {
        'cols': 40,
        'type': 'basic',
        'open_symbol': '\033[1m\033[38;5;1m[\033[0m',
        'close_symbol': '\033[1m\033[38;5;1m]\033[0m',
        'fill_symbol': '\033[1m\033[38;5;196m=\033[0m',
        'unfill_symbol': '\033[1m\033[38;5;1m-\033[0m',
    },
    {
        'cols': 40,
        'type': 'arrow',
        'open_symbol': '\033[1m\033[38;5;2m[\033[0m',
        'close_symbol': '\033[1m\033[38;5;2m]\033[0m',
        'fill_symbol': '\033[1m\033[38;5;28m-\033[0m',
        'arrow_symbol': '\033[1m\033[38;5;28m>\033[0m',
    },
    {
        'cols': 40,
        'type': 'shade',
        'open_symbol': '\033[1m\033[38;5;3m|\033[0m',
        'close_symbol': '\033[1m\033[38;5;3m|\033[0m',
        'fill_symbol': '\033[1m\033[38;5;28m-\033[0m',
        'arrow_symbol': '\033[1m\033[38;5;3m>\033[0m',
    },
    {
        'cols': 40,
        'type': 'basic',
        'open_symbol': '\033[1m\033[38;5;68m|\033[0m',
        'close_symbol': '\033[1m\033[38;5;68m|\033[0m',
        'fill_symbol': '\033[1m\033[38;5;30m█\033[0m',
        'unfill_symbol': '\033[1m\033[38;5;246m█\033[0m',
    },
    {
        'type': 'text'
    },
])

time.sleep(5)

for i in range(101):
    time.sleep(0.05)
    p.update([
        {
        },
        {
            'value': i / 100.0,
            'suffix': '\033[38;5;250m {}MB / 100MB\033[0m'.format(i),
        },
        {
            'value': i / 100.0 * 0.3,
            'suffix': '\033[38;5;250m ETA {}s \033[0m'.format(int(i * 0.1)),
        },
        {
            'value': i / 100.0 * 0.7,
            'suffix': '\033[38;5;250m {} \033[0m'.format(int(i * 0.7)),
        },
        {
            'value': i / 100.0 * 0.9,
            'suffix': '\033[38;5;250m {}% \033[0m'.format(int(i * 0.9)),
        },
        {
        },
    ])

time.sleep(20)
