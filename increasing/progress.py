#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

import sys
import math
import os

BAR_TYPE = [
    'basic',
    'arrow',  # TODO
    'shade',
    'block',
    'rect',  # TODO
    'rotate',  # TODO
    ''
]

BLOCK = [
    u'\u258F'.encode('utf-8'),
    u'\u258E'.encode('utf-8'),
    u'\u258D'.encode('utf-8'),
    u'\u258C'.encode('utf-8'),
    u'\u258B'.encode('utf-8'),
    u'\u258A'.encode('utf-8'),
    u'\u2589'.encode('utf-8'),
    u'\u2588'.encode('utf-8'),
]


class ProgressBar:

    def __init__(self, configs):
        self._configs = self._check_configs(configs)
        self._draw_cnt = 0

    def update_config(self, id, config):
        """Update single configuration by passing index or name.
        """
        if isinstance(id, int):
            self._update_config_by_index(id, config)
        elif isinstance(id, str):
            for i in range(len(self._configs)):
                if self._configs[i]['name'] == id:
                    self._update_config_by_index(i, config)
        else:
            raise TypeError('"id" should be integer index or string name')

        self._draw()

    def update_configs(self, configs):
        """Update the whole configurations.
        """
        if len(configs) != len(self._configs):
            raise ValueError('pass equal length of "configs"')

        for i in range(len(configs)):
            self._update_config_by_index(i, configs[i])

        self._draw()

    def _update_config_by_index(self, index, config):
        """Update the value, prefix, suffix by using index.
        """
        if 'value' in config:
            if not 0 <= config['value'] <= 1:
                raise ValueError('"value" should between 0 and 1')
            self._configs[index]['value'] = config['value']
        if 'prefix' in config:
            self._configs[index]['prefix'] = config['prefix']
        if 'suffix' in config:
            self._configs[index]['suffix'] = config['suffix']

    def _draw(self):
        """Redraw the bars on the terminal.
        """
        out = ''
        for config in self._configs:
            if config['type'] == 'basic' or config['type'] == 'shade':
                fill_cols = int(round(config['value'] * config['cols']))
                out += config['prefix']
                out += config['open_symbol']
                out += config['fill_symbol'] * fill_cols
                out += config['unfill_symbol'] * (config['cols'] - fill_cols)
                out += config['close_symbol']
                out += config['suffix']
                out += '\r\n'
            elif config['type'] == 'block':
                fill_blocks = int(round(config['value'] * config['cols'] * len(BLOCK)))
                out += config['prefix']
                out += config['open_symbol']
                if fill_blocks == 0:
                    out += ' ' * config['cols']
                else:
                    out += BLOCK[-1] * int(fill_blocks / len(BLOCK))
                    if fill_blocks % len(BLOCK) != 0:
                        out += BLOCK[fill_blocks % len(BLOCK)]
                        out += ' ' * (config['cols'] - int(fill_blocks / len(BLOCK)) - 1)
                    else:
                        out += ' ' * (config['cols'] - int(fill_blocks / len(BLOCK)))

                out += config['close_symbol']
                out += config['suffix']
                out += '\r\n'

        if self._draw_cnt:
            # ESC escape CSI to move cursor to previous line
            out = u'\033[F'.encode('utf-8') * len(self._configs) + out
        sys.stdout.write(out)
        sys.stdout.flush()

        self._draw_cnt += 1

    def _check_configs(self, configs):
        """Parse and check the configuration to generate the new configuration.
        """
        if not isinstance(configs, list):
            raise TypeError('"configs" should be a list of dicts')

        names = set()
        n_configs = list()
        for i, config in enumerate(configs):
            if not isinstance(config, dict):
                raise TypeError('"configs" should be a list of dicts')

            n_config = dict()

            # Set index and name
            n_config['index'] = i
            if 'name' in config:
                if config['name'] in names:
                    raise ValueError('duplicate "name" of "{}"'.format(config['name']))
                else:
                    names.add(config['name'])
                    n_config['name'] = config['name']
            else:
                n_config['name'] = None

            # Set the columns, type and name
            n_config['cols'] = int(config.get('cols', 50))
            n_config['fill_cols'] = 0
            if 'type' in config:
                if config['type'] not in BAR_TYPE:
                    raise ValueError('progress bar "type" should be one of {}'.format(BAR_TYPE))
                n_config['type'] = config['type']
            else:
                n_config['type'] = 'basic'

            # Set progress bar symbols based on bar type
            if n_config['type'] == 'basic':
                n_config['open_symbol'] = config.get('open_symbol', '[')
                n_config['close_symbol'] = config.get('close_symbol', ']')
                n_config['fill_symbol'] = config.get('fill_symbol', '=')
                n_config['unfill_symbol'] = config.get('open_symbol', ' ')
            elif n_config['type'] == 'shade':
                n_config['open_symbol'] = config.get('open_symbol', '|')
                n_config['close_symbol'] = config.get('close_symbol', '|')
                n_config['fill_symbol'] = u'\u2588'.encode('utf-8')
                n_config['unfill_symbol'] = u'\u2591'.encode('utf-8')
            elif n_config['type'] == 'block':
                n_config['open_symbol'] = config.get('open_symbol', '|')
                n_config['close_symbol'] = config.get('close_symbol', '|')

            n_config['value'] = 0
            n_config['prefix'] = ''
            n_config['suffix'] = ''
            n_configs.append(n_config)

        return n_configs
