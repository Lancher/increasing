#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import sys

BAR_TYPE = [
    'basic',
    'arrow',
    'shade',
    'block',
    'rect',
    'rotate',
]

BLOCK = [
    '▏',
    '▎',
    '▍',
    '▌',
    '▋',
    '▊',
    '▉',
    '█',
]

INDEF = [
    "-",
    "\\",
    "|",
    "/",
]


class ProgressBar:

    def __init__(self, configs):
        self._configs = self._check_configs(configs)
        self._cnt = 0

    def _check_configs(self, configs):
        """Parse the passing configuration and generate the new configuration.
        """
        if not isinstance(configs, list):
            raise TypeError('"configs" should be a list of dicts')

        new_configs = []
        for config in configs:
            if not isinstance(config, dict):
                raise TypeError('"configs" should be a list of dicts')
            if 'type' not in config:
                new_configs.append(self._check_basic_bar_config(config))
            elif config['type'] == 'basic':
                new_configs.append(self._check_basic_bar_config(config))
            elif config['type'] == 'arrow':
                new_configs.append(self._check_arrow_bar_config(config))
            elif config['type'] == 'shade':
                new_configs.append(self._check_shade_bar_config(config))
            elif config['type'] == 'block':
                new_configs.append(self._check_block_bar_config(config))
            elif config['type'] == 'rect':
                new_configs.append(self._check_rect_bar_config(config))
            elif config['type'] == 'rotate':
                new_configs.append(self._check_rotate_bar_config(config))
        return new_configs

    def _check_basic_bar_config(self, config):
        """Parse the passing basic bar configuration and generate the new configuration.
        """
        new_config = {
            'type': 'basic',
            'open_symbol': config.get('open_symbol', '['),
            'close_symbol': config.get('close_symbol', ']'),
            'fill_symbol': config.get('fill_symbol', '='),
            'unfill_symbol': config.get('fill_symbol', ' '),
            'cols': int(config.get('cols', 50)),
            'value': 0,
            'prefix': '',
            'suffix': '',
        }
        return new_config

    def _check_arrow_bar_config(self, config):
        """Parse the passing arrow bar configuration and generate the new configuration.
        """
        new_config = {
            'type': 'arrow',
            'open_symbol': config.get('open_symbol', '['),
            'close_symbol': config.get('close_symbol', ']'),
            'fill_symbol': config.get('fill_symbol', '='),
            'unfill_symbol': config.get('fill_symbol', ' '),
            'arrow_symbol': config.get('arrow_symbol', '>'),
            'cols': int(config.get('cols', 50)),
            'value': 0,
            'prefix': '',
            'suffix': '',
        }
        return new_config

    def _check_shade_bar_config(self, config):
        """Parse the passing shade bar configuration and generate the new configuration.
        """
        new_config = {
            'type': 'shade',
            'open_symbol': config.get('open_symbol', '|'),
            'close_symbol': config.get('close_symbol', '|'),
            'fill_symbol': '█',
            'unfill_symbol': '░',
            'cols': int(config.get('cols', 50)),
            'value': 0,
            'prefix': '',
            'suffix': '',
        }
        return new_config

    def _check_block_bar_config(self, config):
        """Parse the passing block bar configuration and generate the new configuration.
        """
        new_config = {
            'type': 'block',
            'open_symbol': config.get('open_symbol', '|'),
            'close_symbol': config.get('close_symbol', '|'),
            'cols': int(config.get('cols', 50)),
            'value': 0,
            'prefix': '',
            'suffix': '',
        }
        return new_config

    def _check_rect_bar_config(self, config):
        """Parse the passing rectangle bar configuration and generate the new configuration.
        """
        new_config = {
            'type': 'rect',
            'open_symbol': config.get('open_symbol', '|'),
            'close_symbol': config.get('close_symbol', '|'),
            'fill_symbol': '■',
            'unfill_symbol': config.get('fill_symbol', ' '),
            'cols': int(config.get('cols', 50)),
            'value': 0,
            'prefix': '',
            'suffix': '',
        }
        return new_config

    def _check_rotate_bar_config(self, config):
        """Parse the passing rotatable bar configuration and generate the new configuration.
        """
        new_config = {
            'type': 'rotate',
            'open_symbol': config.get('open_symbol', ''),
            'close_symbol': config.get('close_symbol', ''),
            'done_symbol': config.get('done_symbol', 'ok'),
            'is_done': False,
            'cnt': 0,
            'cols': int(config.get('cols', 50)),
            'value': 0,
            'prefix': '',
            'suffix': '',
        }
        return new_config

    def update(self, configs):
        """Update the whole configurations.
        """
        if len(configs) != len(self._configs):
            raise ValueError('length of "configs" is not matching')

        for i in range(len(configs)):
            self._update_config_by_index(i, configs[i])
        self._write()

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
        if 'is_done' in config:
            self._configs[index]['is_done'] = config['is_done']

    def _render_output(self):
        """Render concatenate string on each different bar types.
        """
        out = ''
        for config in self._configs:
            if config['type'] == 'basic':
                out += self._render_basic_bar_output(config)
            elif config['type'] == 'arrow':
                out += self._render_arrow_bar_output(config)
            elif config['type'] == 'shade':
                out += self._render_basic_bar_output(config)
            elif config['type'] == 'block':
                out += self._render_block_bar_output(config)
            elif config['type'] == 'rect':
                out += self._render_basic_bar_output(config)
            elif config['type'] == 'rotate':
                out += self._render_rotate_bar_output(config)
        # ESC escape CSI to move cursor to previous line, u'\033[F'
        if self._cnt:
            out = '[F' * len(self._configs) + out
        return out

    def _render_basic_bar_output(self, config):
        """Render concatenate string on basic bar type.
        """
        cols = int(round(config['value'] * config['cols']))
        out = config['prefix'] + config['open_symbol'] + config['fill_symbol'] * cols + \
            config['unfill_symbol'] * (config['cols'] - cols) + config['close_symbol'] + \
            config['suffix'] + '\r\n'
        return out

    def _render_arrow_bar_output(self, config):
        """Render concatenate string on arrow bar type.
        """
        cols = int(round(config['value'] * config['cols']))
        out = config['prefix'] + config['open_symbol'] + config['fill_symbol'] * cols
        if config['cols'] - cols > 0:
            out += config['arrow_symbol']
            out += config['unfill_symbol'] * (config['cols'] - cols - 1)
        else:
            out += config['unfill_symbol'] * (config['cols'] - cols)
        out += config['close_symbol'] + config['suffix'] + '\r\n'
        return out

    def _render_block_bar_output(self, config):
        """Render concatenate string on block bar type.
        """
        blocks = int(round(config['value'] * config['cols'] * len(BLOCK)))
        out = config['prefix'] + config['open_symbol']
        if blocks == 0:
            out += ' ' * config['cols']
        else:
            out += BLOCK[-1] * int(blocks / len(BLOCK))
            if blocks % len(BLOCK) != 0:
                out += BLOCK[blocks % len(BLOCK)]
                out += ' ' * (config['cols'] - int(blocks / len(BLOCK)) - 1)
            else:
                out += ' ' * (config['cols'] - int(blocks / len(BLOCK)))
        out += config['close_symbol'] + config['suffix'] + '\r\n'
        return out

    def _render_rotate_bar_output(self, config):
        """Render concatenate string on rotate bar type.
        """
        out = config['prefix'] + config['open_symbol']
        out += config['done_symbol'] if config['is_done'] else INDEF[config['cnt'] % 4]
        out += config['close_symbol'] + config['suffix'] + '\r\n'
        config['cnt'] += 1
        return out

    def _write(self):
        """Write characters to stdout.
        """
        sys.stdout.write(self._render_output())
        sys.stdout.flush()
        self._cnt += 1
